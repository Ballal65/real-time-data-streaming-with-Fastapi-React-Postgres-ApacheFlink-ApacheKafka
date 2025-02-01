import os
from fastapi import Depends
import snowflake.connector as SF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to create and yield a Snowflake connection
def get_snowflake_conn():
    conn = SF.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )
    try:
        yield conn  # Provide connection to the route
    finally:
        conn.close()
