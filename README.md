# Property Planner Web Application

This repository contains a simple property management dashboard built with **FastAPI** and **SQLAlchemy**.  The application allows you to:

* View a dashboard summarising the number and total value of your personal and company properties.
* Add new properties with a friendly form.
* Browse a list of all properties in your portfolio.
* Navigate to placeholders for refinancing and acquisition sections (to be expanded in the future).

The frontend is server‑rendered using Jinja2 templates and includes a custom stylesheet for a clean and professional look.

## Running locally with Docker

Ensure you have Docker installed.  From within the `property_planner` directory run:

```bash
# Build the Docker image
docker build -t property_planner .

# Start the application
docker run -it --rm -p 8000:8000 property_planner
```

Alternatively, use the provided docker‑compose configuration:

```bash
docker-compose up --build
```

The web app will be available at <http://localhost:8000>.  The first run will create a SQLite database file (`property_planner.db`) in the container; it persists across restarts when using the mounted volume in `docker-compose.yml`.

## Project structure

```text
property_planner/
├── app/
│   ├── __init__.py            # Makes the app package importable
│   ├── main.py                # FastAPI application instance and routes
│   ├── database.py            # SQLAlchemy engine and session management
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic models for request/response validation
│   ├── crud.py                # Helper functions for database operations
│   └── routers/               # Placeholders for future route modules
├── templates/                 # Jinja2 templates
│   ├── layout.html
│   ├── dashboard.html
│   ├── add_property.html
│   ├── property_list.html
│   ├── refinancing.html
│   └── acquisition.html
├── static/
│   └── css/
│       └── styles.css
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build configuration
├── docker-compose.yml         # Compose file for local development
└── README.md                  # This file
```

## Extending the application

The current implementation provides a solid skeleton for a more fully‑featured property management system.  Future enhancements might include:

* Authentication and user accounts.
* CRUD operations for acquisitions, refinancing deals, and financial metrics.
* Integration with third‑party APIs for property valuations or mortgage rates.
* Advanced analytics and charts.

Contributions and pull requests are welcome!