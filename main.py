from io import BytesIO
import matplotlib.pyplot as plt

import metrics
from db_connector import DBConnector
from github_service import GithubService

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI()
db_connector = DBConnector()


@app.on_event("startup")
async def startup_event():
    db_connector.initialize_indexes()
    app.github_service = GithubService()
    await app.github_service.start()


@app.on_event("shutdown")
async def shutdown_event():
    print("bay bay")


@app.get("/events")
async def get_events():
    return db_connector.get_all_events()


@app.get("/average_pr_time/{repo:path}")
def average_pr_time(repo: str = None):
    data = db_connector.get_pull_request_events(repo)
    average_pr_time_in_seconds = [
        {"repo": event["_id"], "average_pr_time_in_seconds": metrics.calculate_average_pr_time(event["created_at"])}
        for event in data
    ]
    return average_pr_time_in_seconds


@app.get("/events_count")
@app.get("/events_count/{offset}")
def events_count(offset: int = None):
    fields = {"type"}
    if offset:
        recent_events = db_connector.get_last_n_minutes_events(offset, fields)
    else:
        recent_events = db_connector.get_all_events(fields)

    event_counts = metrics.calculate_events_count(recent_events)
    return event_counts


@app.get("/visualization", response_class=Response)
async def get_visualization():
    events = db_connector.get_all_events({"type"})
    event_counts = metrics.calculate_events_count(events)

    plt.bar(event_counts.keys(), event_counts.values())
    plt.xlabel("Event type")
    plt.ylabel("Count")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
