# metrics.py
from typing import Any, Dict, List
from datetime import datetime
from collections import Counter


def calculate_average_pr_time(pr_times: List[datetime]) -> float | int:
    pr_times.sort()
    diffs = [(pr_times[i + 1] - pr_times[i]).total_seconds() for i in range(len(pr_times) - 1)]
    return sum(diffs) / len(diffs) if diffs else 0


def calculate_events_count(events: List[dict]) -> dict:
    # event_counts = {}
    # for event in events:
    #     event_type = event['type']
    #     if event_type not in event_counts:
    #         event_counts[event_type] = 0
    #     event_counts[event_type] += 1
    event_counts = Counter(event.get("type") for event in events)
    return event_counts


class MetricsService:

    def __init__(self, db):
        self.db = db

    def calculate_metrics(self):
        events = self.db.all()
        total_events = len(events)
        unique_repos = len(set(event['repo']['id'] for event in events))

        return {
            'total_events': total_events,
            'unique_repos': unique_repos
        }
