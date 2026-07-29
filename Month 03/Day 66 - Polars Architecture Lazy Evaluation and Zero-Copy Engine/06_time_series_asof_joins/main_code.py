# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: High-Performance Asof Joins on Temporal Streams
Description: Matches trade executions with the nearest preceding stock quote
             timestamp using Polars join_asof for high-frequency financial datasets.
"""
from datetime import datetime
import polars as pl  # type: ignore


class FinancialAsofJoinEngine:
    @staticmethod
    def align_trades_with_quotes(quotes: pl.DataFrame, trades: pl.DataFrame) -> pl.DataFrame:
        # Execute temporal match finding nearest preceding quote timestamp
        return trades.join_asof(
            quotes,
            on="timestamp",
            by="symbol",
            strategy="backward"
        )


if __name__ == "__main__":
    # Quotes feed
    df_quotes = pl.DataFrame({
        "timestamp": [
            datetime(2026, 7, 25, 10, 0, 0),
            datetime(2026, 7, 25, 10, 0, 5),
            datetime(2026, 7, 25, 10, 0, 10)
        ],
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "bid": [150.0, 150.25, 150.50]
    }).sort("timestamp")
    
    # Trades feed (occurred slightly after quotes)
    df_trades = pl.DataFrame({
        "timestamp": [
            datetime(2026, 7, 25, 10, 0, 2),
            datetime(2026, 7, 25, 10, 0, 8)
        ],
        "symbol": ["AAPL", "AAPL"],
        "trade_price": [150.10, 150.30]
    }).sort("timestamp")
    
    df_aligned = FinancialAsofJoinEngine.align_trades_with_quotes(df_quotes, df_trades)
    
    assert len(df_aligned) == 2
    assert df_aligned["bid"].to_list() == [150.0, 150.25]
    
    print(f"[TASK 06 PASSED] Asof temporal join successfully matched trades to quotes:\n{df_aligned}")