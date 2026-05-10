#!/usr/bin/env python3
"""
MCP Server for PostgreSQL.
Provides SQL query capabilities against a PostgreSQL database.

Usage:
  DATABASE_URL=postgresql://user:pass@host:port/db python3 postgres-server.py
"""

import os
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("❌ mcp package not installed. Run: pip install mcp")
    sys.exit(1)

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)

# Connection config — from env or args (arg takes precedence)
import argparse

parser = argparse.ArgumentParser(description="PostgreSQL MCP Server")
parser.add_argument("--url", help="Database URL (e.g. postgresql://user:pass@host:port/db)")
parser.add_argument("--host", default=os.environ.get("PG_HOST", "localhost"))
parser.add_argument("--port", type=int, default=int(os.environ.get("PG_PORT", "5432")))
parser.add_argument("--user", default=os.environ.get("PG_USER", "postgres"))
parser.add_argument("--password", default=os.environ.get("PG_PASS", "mcp_pass"))
parser.add_argument("--db", default=os.environ.get("PG_DB", "mcp_db"))
args, _ = parser.parse_known_args()


def get_conn():
    if args.url:
        return psycopg2.connect(args.url)
    return psycopg2.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        dbname=args.db,
    )


mcp = FastMCP("PostgreSQL Server")


@mcp.tool()
def pg_list_tables() -> str:
    """List all tables in the current database with schema info."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """)
        rows = cur.fetchall()
        if not rows:
            return "No tables found."
        result = ["| Schema | Table | Type |", "|--------|-------|------|"]
        for s, t, tt in rows:
            result.append(f"| {s} | {t} | {tt} |")
        return "\n".join(result)
    finally:
        conn.close()


@mcp.tool()
def pg_get_schema(table_name: str) -> str:
    """
    Get the schema (columns, types, constraints) for a specific table.

    Args:
        table_name: Name of the table (e.g., 'users', 'public.orders')
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        schema = "public"
        table = table_name
        if "." in table_name:
            schema, table = table_name.split(".", 1)

        cur.execute(
            """
            SELECT
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default,
                tc.constraint_type
            FROM information_schema.columns c
            LEFT JOIN information_schema.key_column_usage k
                ON c.column_name = k.column_name AND c.table_name = k.table_name
                AND c.table_schema = k.table_schema
            LEFT JOIN information_schema.table_constraints tc
                ON k.constraint_name = tc.constraint_name
                AND k.table_name = tc.table_name
                AND k.table_schema = tc.table_schema
            WHERE c.table_name = %s AND c.table_schema = %s
            ORDER BY c.ordinal_position
        """,
            (table, schema),
        )

        rows = cur.fetchall()
        if not rows:
            return f"Table '{table_name}' not found."

        result = [
            f"### Schema: {schema}.{table}\n",
            "| Column | Type | Nullable | Default | Constraint |",
            "|--------|------|----------|---------|------------|",
        ]
        for col, dtype, nullable, default, const in rows:
            result.append(f"| {col} | {dtype} | {nullable} | {default or ''} | {const or ''} |")

        return "\n".join(result)
    finally:
        conn.close()


@mcp.tool()
def pg_query(sql: str, limit: int = 100) -> str:
    """
    Execute a SQL SELECT query and return results as a formatted table.

    Args:
        sql: The SQL SELECT query to execute
        limit: Maximum number of rows to return (default 100, max 1000)
    """
    if not sql.strip().upper().startswith("SELECT"):
        return "❌ Only SELECT queries are allowed for safety."

    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        rows = cur.fetchmany(min(limit, 1000))

        if not rows:
            return "Query returned no results."

        # Format as markdown table
        columns = list(rows[0].keys())
        header = f"| {' | '.join(columns)} |"
        sep = f"| {' | '.join(['---'] * len(columns))} |"

        result_lines = [f"📊 **{len(rows)} rows**\n", header, sep]
        for row in rows:
            values = []
            for col in columns:
                val = row[col]
                if val is None:
                    values.append("NULL")
                else:
                    values.append(str(val)[:80])  # truncate long values
            result_lines.append(f"| {' | '.join(values)} |")

        return "\n".join(result_lines)

    except Exception as e:
        return f"❌ Query error: {e}"
    finally:
        conn.close()


@mcp.tool()
def pg_tables_summary() -> str:
    """Get a summary of all tables with row counts and estimated sizes."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                relname AS table_name,
                n_live_tup AS row_count,
                pg_size_pretty(pg_total_relation_size(relid)) AS total_size
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
        """)
        rows = cur.fetchall()
        if not rows:
            return "No user tables found."

        result = [
            "| Table | Rows (approx) | Size |",
            "|-------|---------------|------|",
        ]
        for t, r, s in rows:
            result.append(f"| {t} | {r:,} | {s} |")

        return "\n".join(result)
    finally:
        conn.close()


if __name__ == "__main__":
    print("🚀 PostgreSQL MCP Server starting...", file=sys.stderr)
    print(f"   Connecting to: {args.host}:{args.port}/{args.db}", file=sys.stderr)
    mcp.run(transport="stdio")
