import duckdb

def connect_duckdb(db_path: str) -> duckdb.DuckDBPyConnection:
    """Connect to DuckDB with performance optimizations."""
    conn = duckdb.connect(db_path)
    
    # Performance optimizations
    conn.execute("PRAGMA memory_limit='2GB'")
    conn.execute("PRAGMA threads=4")
    conn.execute("PRAGMA enable_progress_bar=false")
    
    return conn