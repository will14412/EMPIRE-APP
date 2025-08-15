from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models, database, crud, schemas
from .routers import refinancing, acquisition


# Create database tables on startup if they don't already exist.
models.Base.metadata.create_all(bind=database.engine)

# Instantiate the FastAPI application.
app = FastAPI(title="Property Planner")

# Configure Jinja2 templates directory.
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, images) from the 'static' directory.
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    """Provide a SQLAlchemy database session to path operations."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_dashboard(request: Request, db: Session = Depends(get_db)):
    """Render the dashboard with portfolio summary statistics."""
    summary = crud.portfolio_summary(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "personal_count": summary["personal_count"],
            "company_count": summary["company_count"],
            "total_value": summary["total_value"],
            "company_value": summary["company_value"],
        },
    )


@app.get("/properties", response_class=HTMLResponse)
def list_properties(request: Request, db: Session = Depends(get_db)):
    """Display a table of all properties in the database."""
    properties = crud.get_properties(db)
    return templates.TemplateResponse(
        "property_list.html", {"request": request, "properties": properties}
    )


@app.get("/properties/add", response_class=HTMLResponse)
def add_property_form(request: Request):
    """Render the form for adding a new property."""
    return templates.TemplateResponse("add_property.html", {"request": request})


@app.post("/properties/add")
def add_property(
    request: Request,
    name: str = Form(...),
    value: float = Form(...),
    type: str = Form(...),
    address: str = Form(""),
    db: Session = Depends(get_db),
):
    """Process form submission to create a new property and redirect to the list."""
    # Validate and create a new property record.
    property_in = schemas.PropertyCreate(
        name=name,
        value=value,
        type=schemas.PropertyType(type),
        address=address,
    )
    crud.create_property(db, property_in)
    # Redirect to the property list page after successful creation.
    return RedirectResponse(url="/properties", status_code=303)


# Include placeholder routers for future functionality.
app.include_router(refinancing.router)
app.include_router(acquisition.router)