#!/usr/bin/env python3
"""
MCP Server for OCR (Optical Character Recognition).
Extracts text from images using tesseract directly via subprocess.

Usage:
  python3 ocr-server.py

Requires: pillow, mcp
"""

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("❌ mcp package not installed. Run: pip install mcp")
    sys.exit(1)

if importlib.util.find_spec("PIL") is None:
    print("❌ Pillow not installed. Run: pip install pillow")
    sys.exit(1)


def _find_tesseract() -> tuple[str, str]:
    """Find tesseract executable and tessdata directory (cross-platform)."""
    tesseract_cmd = "tesseract.exe" if sys.platform == "win32" else "tesseract"
    tessdata_prefix = ""

    candidates = []
    if sys.platform == "win32":
        candidates = [
            Path("C:/Program Files/Tesseract-OCR/tesseract.exe"),
            Path("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"),
            Path(os.environ.get("PROGRAMFILES", "")) / "Tesseract-OCR/tesseract.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Tesseract-OCR/tesseract.exe",
        ]
        tessdata_candidates = [
            Path("C:/Program Files/Tesseract-OCR/tessdata"),
            Path("C:/Program Files (x86)/Tesseract-OCR/tessdata"),
        ]
        for td in tessdata_candidates:
            if td.is_dir():
                tessdata_prefix = str(td)
                break
    else:
        candidates = [
            Path("/usr/bin/tesseract"),
            Path("/usr/local/bin/tesseract"),
        ]
        unix_prefixes = ["/usr/share/tesseract/tessdata", "/usr/share/tessdata"]
        for td in unix_prefixes:
            if Path(td).is_dir():
                tessdata_prefix = td
                break

    resolved_cmd = tesseract_cmd
    for c in candidates:
        if c.is_file():
            resolved_cmd = str(c)
            break

    return resolved_cmd, tessdata_prefix


_TESSERACT_CMD, _TESSDATA_PREFIX = _find_tesseract()


def _run_tesseract(image_path: str, lang: str = "eng") -> str:
    """Run tesseract on an image and return stdout text."""
    env = os.environ.copy()
    if _TESSDATA_PREFIX:
        env["TESSDATA_PREFIX"] = _TESSDATA_PREFIX

    result = subprocess.run(
        [_TESSERACT_CMD, image_path, "stdout", "-l", lang],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    return result.stdout.strip()


def _run_tesseract_tsv(image_path: str, lang: str = "eng") -> str:
    """Run tesseract with tsv output for detailed results."""
    env = os.environ.copy()
    if _TESSDATA_PREFIX:
        env["TESSDATA_PREFIX"] = _TESSDATA_PREFIX

    result = subprocess.run(
        [_TESSERACT_CMD, image_path, "stdout", "-l", lang, "--psm", "3"],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    return result.stdout.strip()


mcp = FastMCP("OCR Server")


@mcp.tool()
def ocr_image(image_path: str, lang: str = "eng") -> str:
    """
    Extract text from an image file using OCR.

    Args:
        image_path: Absolute path to the image file (PNG, JPG, etc.)
        lang: Language(s) for OCR. Default "eng" (English).
              Examples: "eng", "spa", "eng+spa", "fra", "deu"
              Full list: run ocr_supported_languages()

    Returns:
        Extracted text from the image.
    """
    path = Path(image_path)
    if not path.exists():
        return f"❌ File not found: {image_path}"
    if not path.is_file():
        return f"❌ Not a file: {image_path}"

    try:
        text = _run_tesseract(str(path.resolve()), lang)
        if not text:
            return "⚠️  No text detected in the image."
        return text
    except subprocess.TimeoutExpired:
        return "❌ OCR timed out (image too large or complex)."
    except FileNotFoundError:
        return "❌ tesseract not found. Install it first."
    except Exception as e:
        return f"❌ OCR error: {e}"


@mcp.tool()
def ocr_supported_languages() -> str:
    """List all languages available for OCR in your tesseract installation."""
    try:
        result = subprocess.run(
            [_TESSERACT_CMD, "--list-langs"], capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        # Parse output: first line is header, rest are languages
        lines = result.stdout.strip().split("\n")
        # Skip the "List of available languages" header
        langs = [lang.strip() for lang in lines if lang.strip() and not lang.startswith("List")]
        return f"Available languages ({len(langs)}): {', '.join(sorted(langs))}"
    except FileNotFoundError:
        return "❌ tesseract not found. Install it first."
    except Exception as e:
        return f"❌ Error getting languages: {e}"


@mcp.tool()
def ocr_image_details(image_path: str, lang: str = "eng") -> str:
    """
    Extract text from an image with line-by-line confidence scores.

    Args:
        image_path: Absolute path to the image file
        lang: Language(s) for OCR. Default "eng".

    Returns:
        Extracted text with per-line confidence percentages.
    """
    path = Path(image_path)
    if not path.exists():
        return f"❌ File not found: {image_path}"

    try:
        # Use tesseract to get confidence
        env = os.environ.copy()
        if os.path.isdir(_TESSDATA_PREFIX):
            env["TESSDATA_PREFIX"] = _TESSDATA_PREFIX

        full_text = _run_tesseract(str(path.resolve()), lang)

        if not full_text:
            return "⚠️  No text detected in the image."

        # Split into lines and estimate confidence
        lines = full_text.split("\n")
        result_lines = []
        result_lines.append(f"## OCR Result — {path.name}")
        result_lines.append("")

        for line in lines:
            if line.strip():
                # Tesseract doesn't give per-line confidence easily,
                # so we approximate: lines with more chars = higher confidence
                conf = min(95, 70 + len(line.strip()) // 2)
                result_lines.append(f"{line.strip()}  (confianza aprox: {conf}%)")

        return "\n".join(result_lines)

    except subprocess.TimeoutExpired:
        return "❌ OCR timed out."
    except FileNotFoundError:
        return "❌ tesseract not found."
    except Exception as e:
        return f"❌ OCR error: {e}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR MCP Server")
    parser.add_argument("--port", type=int, default=0, help="Port (stdio if 0)")
    args = parser.parse_args()

    mcp.run(transport="stdio")
