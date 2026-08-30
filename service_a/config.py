import os

SERVICE_B_URL = os.getenv(
    "SERVICE_B_URL",
    "http://localhost:8001"
)

SERVICE_B_REPLICA_URL = os.getenv(
    "SERVICE_B_REPLICA_URL",
    "http://localhost:8002"
)

LOG_FILE = "service_a/logs/service_a.log"