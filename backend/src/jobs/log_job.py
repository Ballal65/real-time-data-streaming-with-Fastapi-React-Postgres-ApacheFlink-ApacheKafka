import os
import requests
import json
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, DataTypes, StreamTableEnvironment
from pyflink.table.udf import ScalarFunction, udf


# UDF to get location from IP
class GetLocation(ScalarFunction):
    def eval(self, ip_address):
        url = "https://api.ip2location.io"
        response = requests.get(url, params={
            'ip': ip_address,
            'key': os.environ.get("IP_CODING_KEY")
        })

        if response.status_code != 200:
            return json.dumps({})

        data = response.json()
        country = data.get('country_code', '')
        state = data.get('region_name', '')
        city = data.get('city_name', '')

        return json.dumps({'country': country, 'state': state, 'city': city})


# Register UDF
get_location = udf(GetLocation(), result_type=DataTypes.STRING())

def create_events_source_kafka(t_env):
    table_name = "events"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            client_host VARCHAR,
            http_method VARCHAR,
            url VARCHAR,
            event_time STRING
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = '{os.environ.get('KAFKA_BROKER')}',
            'topic' = '{os.environ.get('KAFKA_TOPIC')}',
            'properties.group.id' = '{os.environ.get('KAFKA_GROUP')}',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        );
    """
    print(f"Kafka Source DDL: \n{source_ddl}")
    t_env.execute_sql(source_ddl)
    return table_name

def create_processed_events_sink_postgres(t_env):
    table_name = 'processed_events'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            client_host VARCHAR,
            http_method VARCHAR,
            url VARCHAR,
            event_time TIMESTAMP(3)
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{os.environ.get("POSTGRES_URL")}',
            'table-name' = '{table_name}',
            'username' = '{os.environ.get("POSTGRES_USER")}',
            'password' = '{os.environ.get("POSTGRES_PASSWORD")}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    print(f"Postgres Sink DDL: \n{sink_ddl}")
    t_env.execute_sql(sink_ddl)
    return table_name

def log_processing():
    try:
        print('Starting Flink job...')

        # Set up the environment
        env = StreamExecutionEnvironment.get_execution_environment()
        env.enable_checkpointing(10000)
        env.set_parallelism(1)

        settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
        t_env = StreamTableEnvironment.create(env, environment_settings=settings)

        # Register the UDF
        t_env.create_temporary_function("get_location", get_location)

        # Create source and sink tables
        source_table = create_events_source_kafka(t_env)
        postgres_sink = create_processed_events_sink_postgres(t_env)

        # Insert data into Postgres with timestamp conversion
        print("Inserting data into Postgres...")
        t_env.execute_sql(
            f"""
            INSERT INTO {postgres_sink}
            SELECT
                client_host,
                http_method,
                url,
                TO_TIMESTAMP(SUBSTRING(event_time, 1, 26), 'yyyy-MM-dd''T''HH:mm:ss.SSSSSS') AS event_time
            FROM {source_table}
            """
        ).wait()

        print("Flink job completed!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    log_processing()
