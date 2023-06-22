# Github Stream Service

Github Stream Service is a Python application built with FastAPI and MongoDB. It constantly connects to the GitHub API to fetch and analyze the latest events on GitHub. Then, it provides the computed metrics through a REST API.

## Features

1. **Stream Events**: The application continuously connects to the GitHub API to fetch the latest events.
2. **Calculate Metrics**: The application calculates the average time between pull requests for a given repository and the total number of events grouped by the event type.
3. **API Endpoints**: The application provides these metrics through REST API endpoints.
4. **Data Visualization**: The application also provides a visualization of the total number of events grouped by the event type.

## Installation and Running

1. Clone the repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Set up MongoDB and start it on your local machine.
4. Run the application with `uvicorn main:app`.

## API Endpoints

- `/events`: Returns all the events fetched from the GitHub API.
- `/average_pr_time/{repo}`: Returns the average time between pull requests for the specified repository. If no repository is specified, it returns the average time between pull requests for all repositories.
- `/events_count`: Returns the total number of events grouped by the event type.
- `/events_count/{offset}`: Returns the total number of events grouped by the event type in the last `offset` minutes.
- `/visualization`: Returns a visualization of the total number of events grouped by the event type in png format.

## Dependencies

- MongoDB

