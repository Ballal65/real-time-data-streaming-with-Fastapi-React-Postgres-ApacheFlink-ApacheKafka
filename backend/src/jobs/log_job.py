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
            url VARCHAR
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = '{os.environ.get('KAFKA_BROKER')}',
            'topic' = '{os.environ.get('KAFKA_TOPIC')}',
            'properties.group.id' = '{os.environ.get('KAFKA_GROUP')}',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name


def create_processed_events_sink_postgres(t_env):
    table_name = 'user_logs'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            client_host VARCHAR,
            http_method VARCHAR,
            url VARCHAR
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{os.environ.get("POSTGRES_URL")}',
            'table-name' = '{table_name}',
            'username' = '{os.environ.get("POSTGRES_USER")}',
            'password' = '{os.environ.get("POSTGRES_PASSWORD")}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name


def log_processing():
    try:
        print('Starting Flink job...')

        # Set up the environment
        env = StreamExecutionEnvironment.get_execution_environment()
        env.enable_checkpointing(10000)
        env.set_parallelism(1)
        print(env)
        settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
        t_env = StreamTableEnvironment.create(env, environment_settings=settings)
        print(settings)
        # Register the UDF
        t_env.create_temporary_function("get_location", get_location)

        # Create source table
        source_table = create_events_source_kafka(t_env)
        print(source_table)
        postgres_sink = create_processed_events_sink_postgres(t_env)
        print(postgres_sink)
        print('loading into postgres')
        t_env.execute_sql(
            f"""
            INSERT INTO {postgres_sink}
            SELECT
                client_host,
                http_method,
                url
            FROM {source_table}
            """
        ).wait()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    


    # Execute the SQL query


    # Execute SQL to read from the source
    result = t_env.execute_sql(f"SELECT * FROM {source_table}")
    print("Reading events from Kafka...")
    print(result.collect())

    print("Flink job completed!")


if __name__ == "__main__":
    log_processing()
