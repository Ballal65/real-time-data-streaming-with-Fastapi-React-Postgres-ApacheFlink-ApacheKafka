from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import datetime, timedelta
import pandas as pd
import snowflake.connector
from app.snowflake_connection import get_snowflake_conn

router = APIRouter(tags=['NIFTY DASHBOARD'], prefix='/nifty')

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

