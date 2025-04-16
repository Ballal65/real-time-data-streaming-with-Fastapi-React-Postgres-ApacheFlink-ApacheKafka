from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import datetime, timedelta
import pandas as pd
import snowflake.connector
from app.snowflake_connection import get_snowflake_conn
from typing import List, Dict

router = APIRouter(tags=['NIFTY DASHBOARD'], prefix='/nifty')

@router.get('/get-nifty-graph/{date}/{interval}', status_code=200)
async def get_nifty_graph(date: str, interval: str, db: Session = Depends(get_db)) -> List[Dict]:
    """
    Fetch NIFTY candlestick data based on the selected date and interval (interval in minutes).
    """
    try:
        # Validate and parse the date
        try:
            selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD."
            )

        # Validate and parse the interval (interval in minutes)
        try:
            interval_minutes = int(interval)
            if interval_minutes not in [5, 15, 30, 60]:
                raise ValueError
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid interval. Use 5, 15, 30, or 60 minutes."
            )

        # Define market hours (9:15 AM to 3:30 PM) using the selected date
        market_start = f"{date} 09:15:00"
        market_end = f"{date} 15:30:00"

        # SQL query to generate candlestick data with dynamic date and interval using bindparam
        query = text(f"""
            WITH intervals AS (
                SELECT generate_series(
                    '{market_start}'::timestamp,
                    '{market_end}'::timestamp,
                    interval '1 minute' * {interval_minutes}
                ) AS candle_start
            ),
            nifty_with_interval AS (
                SELECT 
                    datetime,
                    value,
                    date_trunc('minute', datetime) - 
                        (EXTRACT(MINUTE FROM datetime)::int % {interval_minutes}) * interval '1 minute' AS candle_start
                FROM nifty
                WHERE datetime >= '{market_start}'::timestamp
                AND datetime <= '{market_end}'::timestamp
            ),
            candlestick_data AS (
                SELECT 
                    candle_start,
                    FIRST_VALUE(value) OVER (
                        PARTITION BY candle_start 
                        ORDER BY datetime
                    ) AS open,
                    MAX(value) OVER (
                        PARTITION BY candle_start
                    ) AS high,
                    MIN(value) OVER (
                        PARTITION BY candle_start
                    ) AS low,
                    LAST_VALUE(value) OVER (
                        PARTITION BY candle_start 
                        ORDER BY datetime
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS close
                FROM nifty_with_interval
            )
            SELECT DISTINCT
                i.candle_start,
                COALESCE(d.open, NULL) AS open,
                COALESCE(d.high, NULL) AS high,
                COALESCE(d.low, NULL) AS low,
                COALESCE(d.close, NULL) AS close
            FROM intervals i
            LEFT JOIN candlestick_data d
            ON i.candle_start = d.candle_start
            ORDER BY i.candle_start;
        """)

        # Execute the query without parameters since values are already injected in f-string
        results = db.execute(query).fetchall()

        # Convert results to a JSON-serializable format
        candlestick_data = [
            {
                "time": row.candle_start.isoformat(),  # Convert timestamp to ISO format for JSON
                "open": float(row.open) if row.open is not None else None,
                "high": float(row.high) if row.high is not None else None,
                "low": float(row.low) if row.low is not None else None,
                "close": float(row.close) if row.close is not None else None
            }
            for row in results
        ]
        print(candlestick_data)
        return candlestick_data

    except SQLAlchemyError as e:
        print("Database error:", e)
        raise HTTPException(
            status_code=500,
            detail="Error fetching NIFTY data."
        )
    except Exception as e:
        print("Unexpected error:", e)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )

'''
@router.get('/get-candlestick/{date}/{candle_minutes}', status_code=status.HTTP_200_OK)
async def min_date(date: str, candle_minutes: int,conn: snowflake.connector.connection = Depends(get_snowflake_conn)):
    try:
        query = f"""
        WITH X_AXIS AS (
            SELECT 
                VALUE AS price, 
                DATETIME AS time, 
                DATETIME::DATE AS date,
                TIME_SLICE(DATETIME, {candle_minutes}, 'MINUTE') AS candle_time  -- Groups into 5-min intervals
            FROM NIFTY.PUBLIC.NIFTY50
            WHERE DATETIME::DATE = '{date}'
        ),
        CANDLES AS (
            SELECT 
                candle_time,
                FIRST_VALUE(price) OVER (PARTITION BY candle_time ORDER BY time) AS open, -- First value in the 5-min interval
                MAX(price) OVER (PARTITION BY candle_time) AS high,  -- Maximum price in the 5-min interval
                MIN(price) OVER (PARTITION BY candle_time) AS low,   -- Minimum price in the 5-min interval
                LAST_VALUE(price) OVER (PARTITION BY candle_time ORDER BY time ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS close  -- Last value in the 5-min interval
            FROM X_AXIS
        )
        SELECT DISTINCT candle_time, open, high, low, close
        FROM CANDLES
        ORDER BY candle_time;
        """
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        if result:
            return {"days_data": result}
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding vendor: {str(e)}"
        )


'''
