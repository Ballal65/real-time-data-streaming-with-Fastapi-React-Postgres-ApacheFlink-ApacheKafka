import sys
import json
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vendors, jre, nifty_dashboard #, auth
from fastapi.requests import Request
from confluent_kafka import Producer
from app.database import Base, engine
import datetime
import pytz

#If we don't import this FastAPI will not create a table
from app.models import Vendor 

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'fastapi-producer',
    'acks': 'all',
    'compression.type': 'gzip',
    'linger.ms': 5,
    'batch.size': 16384
}
producer = Producer(producer_config)

app = FastAPI()

#Binding the database with main.py
Base.metadata.create_all(bind=engine)

app.include_router(vendors.router)
app.include_router(jre.router)
app.include_router(nifty_dashboard.router)
#app.include_router(auth.router)
# CORS origins
ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://139.59.87.2:3000",
    "http://157.245.104.57:3000"
    # Add other origins as needed
]

#Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log request data
@app.middleware("http")
async def log_request_data(request: Request, call_next):
    # Extract request metadata
    client_host = request.client.host
    http_method = request.method
    url = request.url.path
    headers = dict(request.headers)

    # Convert timestamp to IST
    ist_timezone = pytz.timezone("Asia/Kolkata")
    event_time = datetime.datetime.now(ist_timezone).isoformat()

    # Log the request metadata
    #print(f"Client Host: {client_host}")
    #print(f"Method: {http_method}")
    #print(f"URL: {url}")
    #print(f"Headers: {headers}")
    #print(f"Event Time: {event_time}")
    # Process the request and get the response

    event_message = {
        "client_host": client_host,
        "http_method": http_method,
        "url": url,
        #"headers": headers,
        "event_time": event_time
    }

    # Convert the event message to a JSON string
    event_message_json = json.dumps(event_message)

    # Send the message to Kafka
    producer.produce('ui-event-log', key=url, value=event_message_json)
    producer.flush()

    response = await call_next(request)
    return response

@app.get("/")
async def get_message():
    return {"Message": "Hello from FastAPI."}

if __name__ == "__main__":
    print(f"By default reload state is False.")
    print("Available CLI argument: Reload state (True/False)")

    args = sys.argv[1:]
    reload = False

    if len(args) == 1:
        if args[0].lower() == 'true':
            reload = True
    print(f"Reload State: {reload}")

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=reload)
