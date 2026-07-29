# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Advanced OLAP SQL Window Functions
Description: Demonstrates DuckDB execution of complex SQL analytical window functions 
             including ROW_NUMBER(), LAG(), and cumulative moving averages.
"""
import duckdb  # type: ignore


class SQLAnalyticsEngine:
    def __init__(self):
        self.conn = duckdb.connect(database=":memory:")

    def run_window_analytics() -> list:
        conn = duckdb.connect(database=":memory:")
        conn.execute("""
            CREATE TABLE sales (
                dept VARCHAR,
                sale_date DATE,
                amount DOUBLE
            );
            INSERT INTO sales VALUES 
                ('ENG', '2026-07-01', 100.0),
                ('ENG', '2026-07-02', 150.0),
                ('HR',  '2026-07-01', 80.0),
                ('HR',  '2026-07-02', 90.0);
        """)
        
        query = """
            SELECT 
                dept,
                sale_date,
                amount,
                AVG(amount) OVER (PARTITION BY dept ORDER BY sale_date) AS running_avg,
                LAG(amount, 1) OVER (PARTITION BY dept ORDER BY sale_date) AS prev_amount
            FROM sales
            ORDER BY dept, sale_date;
        """
        return conn.execute(query).fetchall()


if __name__ == "__main__":
    records = SQLAnalyticsEngine.run_window_analytics()
    
    # Verify running average and LAG values for ENG department row 2
    eng_row_2 = records[1]
    assert eng_row_2[0] == "ENG"
    assert eng_row_2[3] == 125.0  # (100 + 150) / 2
    assert eng_row_2[4] == 100.0  # Previous row amount
    
    print("[TASK 05 PASSED] DuckDB OLAP window analytics (running_avg, lag) computed correctly.")