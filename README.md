# ai_programs
Marks of students 

## Requirements

### Software
- Python 3.10 or later
- FastAPI
- Uvicorn

### Functional Requirements
- Create, list, retrieve, update, and delete academic tasks through a REST API.
- Each task has a unique ID, title, description, priority, status, and optional due date.
- A task title is required and must be between 1 and 200 characters.
- Priority must be `low`, `medium`, or `high`.
- Status must be `pending`, `in_progress`, or `completed`.
- Due dates are optional and must use the `YYYY-MM-DD` format.
- Return `404 Not Found` when a requested task does not exist.
- Reject invalid request data.

### API Endpoints
- `POST /tasks` — create a task
- `GET /tasks` — list all tasks
- `GET /tasks/{task_id}` — retrieve a task by ID
- `PATCH /tasks/{task_id}` — update a task
- `DELETE /tasks/{task_id}` — delete a task

### Installation and Run
Install the dependencies:

    python -m pip install fastapi uvicorn

Start the server from the project folder:

    python -m uvicorn data_model:app --reload

Open `http://127.0.0.1:8000/docs` to explore and test the API.

### Storage
Tasks are stored in memory and are cleared when the server stops.
