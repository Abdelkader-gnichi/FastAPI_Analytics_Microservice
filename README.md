# FastAPI Analytics API

A high-performance FastAPI microservice designed for collecting and analyzing time-series event data. It leverages TimescaleDB for efficient storage and querying of analytics events, making it suitable for tracking user interactions, application performance metrics, or other time-sensitive data.


https://github.com/user-attachments/assets/8e8a999d-3a02-4311-8940-0c14ba726b56


https://github.com/user-attachments/assets/7190345f-52a7-45d2-94b2-e199c6ebac72


## Features

*   **Event Tracking:** Log events via a simple POST request, capturing details like page visited, user agent, IP address, session ID, and event duration.
*   **Aggregated Analytics:** Retrieve aggregated event data grouped by customizable time buckets (e.g., '1 day', '1 hour').
*   **Data Filtering:** Filter aggregated results by specific pages.
*   **OS Detection:** Automatically infers the Operating System (Windows, MacOS, iOS, Android, Linux, Other) from the User-Agent string during aggregation.
*   **Time-Series Optimized:** Utilizes TimescaleDB hypertables and `time_bucket` hyperfunctions for efficient time-based data storage and querying.
*   **Data Validation:** Employs Pydantic and SQLModel for robust request/response data validation and ORM capabilities.
*   **Asynchronous Ready:** Built on FastAPI, supporting asynchronous operations (though current routes are synchronous).
*   **Containerized:** Includes `Dockerfile` and `docker-compose.yml` for easy setup and deployment using Docker.
*   **Database Initialization:** Automatically initializes the database and creates TimescaleDB hypertables on startup.
*   **CORS Enabled:** Configured with FastAPI's CORS middleware (currently allowing all origins).
*   **Deployment Ready:** Includes configuration for deployment on platforms like Railway (`railway.json`).

## Technology Stack

*   **Backend Framework:** FastAPI
*   **Database:** PostgreSQL with TimescaleDB Extension
*   **ORM / Data Validation:** SQLModel
*   **Web Server:** Uvicorn (managed by Gunicorn in Docker)
*   **Containerization:** Docker, Docker Compose
*   **Configuration:** python-decouple
*   **Language:** Python 3.12
*   **Dependency Management:** pip (using `uv` in Docker build)

## Project Structure

```
Project Root
├── boot/
│   └── docker-run.sh              # Startup script, typically used with Docker
│
├── docker-compose.yml             # Docker Compose configuration file
├── Dockerfile                     # Instructions to build the Docker image
│
├── .env                           # Environment variables for local development
├── .env.compose                   # Environment variables specifically for Docker Compose
│
├── notebooks/                     # Jupyter notebooks for testing and interaction
│
├── requirements.txt               # List of Python dependencies
│
├── railway.json                   # Railway deployment configuration file
│
├── src/                           # Main source code directory
│   ├── alembic/                   # (Optional) Alembic migrations for database versioning
│   ├── api/                       # API-related modules
│   │   ├── common/                # Shared utilities and models (e.g., BaseModel, timestamps)
│   │   ├── db/                    # Database configuration, session, and initialization
│   │   └── events/                # Event-specific logic, models, and routing
│   └── main.py                    # Entry point of the FastAPI application
│
└── README.md                      # Project documentation

```
## API Endpoints

### Events

*   **`POST /api/events/`**: Create a new event.
    *   **Request Body:** `EventCreateSchema`
        ```json
        {
          "page": "/homepage",
          "ip_address": "192.168.1.1",
          "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
          "referrer": "https://google.com",
          "session_id": "xyz789",
          "duration": 15, // Optional, in seconds
          "description": "User viewed homepage" // Optional
        }
        ```
    *   **Response:** `200 OK` - `EventModel` (including generated `id` and `time`)

*   **`GET /api/events/`**: Get aggregated event data.
    *   **Query Parameters:**
        *   `duration` (str, optional, default: '1 day'): The time bucket duration (e.g., '1 hour', '1 day', '1 week'). Must be a valid PostgreSQL interval string.
        *   `pages` (List[str], optional): A list of page paths to filter by. If not provided, defaults to a predefined list (`DEFAULT_LOOKUP_PAGES`). Example: `?pages=/&pages=/about`
    *   **Response:** `200 OK` - `List[EventBucketSchema]`
        ```json
        [
          {
            "bucket": "2023-10-27T00:00:00", // Start time of the bucket
            "page": "/",
            "operating_system": "Windows",
            "avg_duration": 12.5,
            "count": 50
          },
          {
            "bucket": "2023-10-27T00:00:00",
            "page": "/about",
            "operating_system": "MacOS",
            "avg_duration": 25.0,
            "count": 15
          }
          // ... more buckets/pages/os combinations
        ]
        ```
        *(Note: `ua` field in `EventBucketSchema` seems unused in the current aggregation query but is defined in the schema)*

*   **`GET /api/events/{event_id}/`**: Get a specific event by its UUID.
    *   **Path Parameter:** `event_id` (UUID)
    *   **Response:** `200 OK` - `EventModel` | `404 Not Found`

### General

*   **`GET /`**: Simple greeting endpoint.
    *   **Response:** `200 OK` - `{"hello": "world"}`
*   **`GET /healthz`**: Health check endpoint for monitoring.
    *   **Response:** `200 OK` - `{"status": "ok"}`

## Setup and Installation

### Prerequisites

*   Docker
*   Docker Compose
*   Python 3.12 (if running locally without Docker)
*   Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Abdelkader-gnichi/FastAPI_Analytics_Microservice.git
    cd FastAPI_Analytics_Microservice
    ```

2.  **Configure Environment Variables:**
    *   Copy the example environment file (if one exists) or create `.env` and `.env.compose` files.
    *   Populate them with your database credentials and other settings based on the structure in `src/api/db/configs.py` and `docker-compose.yml`. Essential variables:
        *   `POSTGRES_USER`
        *   `POSTGRES_PASSWORD`
        *   `POSTGRES_DB`
        *   `POSTGRES_HOST` (use `timescale_pg_db` for Docker Compose)
        *   `POSTGRES_PORT` (usually `5432`)
        *   `PORT` (e.g., `8002` for the FastAPI app)
        *   `DATABASE_URL` (can be auto-constructed if other `POSTGRES_*` vars are set, or set explicitly)

3.  **Build and Run with Docker Compose (Recommended):**
    This method starts both the FastAPI application and the TimescaleDB database container.
    ```bash
    docker-compose up --build
    ```
    The API will be accessible at `http://localhost:PORT` (e.g., `http://localhost:8002` if `PORT=8002`). The database initialization (`init_db`) will run automatically on app startup.

4.  **Running Locally (Without Docker):**
    *   Ensure you have a running PostgreSQL instance with the TimescaleDB extension enabled and configured in your `.env` file (`POSTGRES_HOST` should point to your local or remote DB host).
    *   Install `uv` if not installed, it is way fast than pip:
        ```bash
        pip install uv
        ```
    *   Create a virtual environment:
        ```bash
        uv venv
        source venv/bin/activate # On Windows: venv\Scripts\activate
        ```
    *   Install dependencies:
        ```bash
        uv pip install -r requirements.txt
        # Or if you use pip installed:
        #pip install -r requirements.txt
        ```
    *   Run the FastAPI application:
        ```bash
        # Ensure you are in the src directory or adjust the path to main:app
        cd src
        uvicorn main:app --reload --port ${PORT:-8002} --host 0.0.0.0
        # Or without reload for production-like run:
        # gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8002} main:app
        ```

## Configuration

Configuration is handled via environment variables, loaded using `python-decouple`. Key variables are defined in `src/api/db/configs.py` and expected in the environment or `.env` file.

*   `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`: Database connection details.
*   `DATABASE_URL`: Alternatively, provide the full database connection string.
*   `PORT`: The port on which the FastAPI application will run.

## Deployment

This project is configured for deployment using Docker.

*   **Railway:** A `railway.json` file is included, configured to build using the `Dockerfile` and defining health check endpoints. Ensure your Railway environment variables match the required configuration variables.
*   **Other Platforms:** The `Dockerfile` can be used to build an image for deployment on other container-supporting platforms (e.g., AWS ECS, Google Cloud Run, Kubernetes). Ensure the necessary environment variables are provided in the deployment environment. The `boot/docker-run.sh` script uses Gunicorn to run the application inside the container.

## Testing

The `notebooks/` directory contains Jupyter notebooks that can be used to interact with and test the API endpoints (e.g., sending sample events, querying aggregated data). Ensure the API is running before executing the notebooks.

---

## Contributing

We welcome contributions to this project! To contribute, please follow these steps:

1.  **Fork** the repository on GitHub.
2.  **Clone** your fork to your local machine:
    ```bash
    git clone https://github.com/YOUR_USERNAME/your-repository-name.git
    cd your-repository-name
    ```
    *(Replace `YOUR_USERNAME` and `your-repository-name`)*
3.  Create a **new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-descriptive-feature-name
    ```
    *(Use a descriptive branch name, e.g., `feature/add-browser-detection` or `fix/aggregation-query-error`)*
4.  Make your **changes** and **commit** them with clear, concise messages. It's helpful to follow conventional commit formats if possible (e.g., `feat: ...`, `fix: ...`, `docs: ...`).
    ```bash
    # Make your code changes
    git add .
    git commit -m "feat: Add user browser detection to aggregation"
    ```
5.  **Push** your changes to your forked repository:
    ```bash
    git push origin feature/your-descriptive-feature-name
    ```
6.  Submit a **Pull Request** (PR) from your feature branch on your fork to the `main` (or appropriate target) branch of the original repository.
    *   Clearly describe the changes you've made and why.
    *   Link any relevant issues if applicable (e.g., `Closes #123`).

Please ensure your code adheres to the existing style and conventions. Add tests or documentation where appropriate.

Thank you for helping improve the project!

---

## License

This project is licensed under the **MIT License**.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions outlined in the license. A copy of the license is often included as a `LICENSE` file in the repository.
