import json
from bson.json_util import dumps
from pymongo import MongoClient, ASCENDING
from config import mongodb_config as mongo
from datetime import datetime, timezone, timedelta


class DBConnector:

    def __init__(self):
        self.client = MongoClient(f"mongodb://{mongo['username']}:{mongo['password']}@{mongo['hostname']}:27017/")
        self.db = self.client[mongo['database']]
        self.events_collection = self.db['events']

    def add_event(self, event):
        event['created_at'] = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        if self.is_event_exists(event['id']):
            return False
        else:
            self.events_collection.insert_one(event)
            return True

    def get_event(self, event_id):
        return self.events_collection.find_one({'id': event_id})

    def get_events_by_repo(self, repo_name):
        return list(self.events_collection.find({'repo.name': repo_name}))

    def get_all_events(self, fields=dict):
        return json.loads(dumps(self.events_collection.find({},  fields if fields else {})))

    def get_pull_request_events_by_repo(self, repo):
        self.events_collection.find({'type': 'PullRequestEvent', 'repo.name': repo})

    def get_pull_request_events(self, repo):

        match = {"type": "PullRequestEvent"}

        if repo:
            match["repo.name"] = repo

        pull_request_events = self.events_collection.aggregate([
            {"$match": match},
            {"$group": {"_id": "$repo.name", "count": {"$sum": 1}, "created_at": {"$push": "$created_at"}}},
            {"$match": {"count": {"$gt": 1}}}
        ])

        return list(pull_request_events)

    def get_last_n_minutes_events(self, minutes, fields=None):
        time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
        return list(self.events_collection.find({'created_at': {'$gte': time_threshold}}, fields if fields else {}))

    def is_event_exists(self, event_id):
        return self.events_collection.find_one({'id': event_id}) is not None

    def initialize_indexes(self):
        self.events_collection.create_index([('id', ASCENDING)], unique=True)
