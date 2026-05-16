@echo off
REM Lend.Ai — Pre-push hook (Windows)
REM REGLA FUNDAMENTAL: tests must pass before push

echo.
echo   ==============================================
echo      RUNNING TESTS BEFORE PUSH...
echo   ==============================================
echo.

cd /d "%~dp0..\.."

python -m pytest tests/ -q --tb=short
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo   ==============================================
    echo      TESTS FAILED -- PUSH BLOCKED
    echo      Fix the failing tests before pushing again.
    echo   ==============================================
    exit /b 1
)

echo.
echo   ==============================================
echo      ALL TESTS PASSED -- PUSHING
echo   ==============================================
echo.
