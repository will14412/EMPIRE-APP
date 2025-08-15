from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models, database, crud, schemas
from .routers import refinancing, acquisition, stats


# Create database tables and upgrade schema if needed on startup.
database.init_db()

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
def read_dashboard(
    request: Request, period: str = "month", db: Session = Depends(get_db)
):
    """Render the dashboard with portfolio summary statistics."""
    summary = crud.portfolio_summary(db, period=period)
    return templates.TemplateResponse("dashboard.html", {"request": request, **summary})


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
async def add_property(request: Request, db: Session = Depends(get_db)):
    """Process form submission to create a new property and redirect to the list."""
    form = await request.form()
    data = {k: (v if v != "" else None) for k, v in dict(form).items()}
    if "has_mortgage" in data:
        data["has_mortgage"] = data["has_mortgage"] in {"yes", "true", "on", "1"}
    property_in = schemas.PropertyCreate(**data)
    crud.create_property(db, property_in)
    return RedirectResponse(url="/properties", status_code=303)


@app.get("/properties/{property_id}", response_class=HTMLResponse)
def view_property(property_id: int, request: Request, db: Session = Depends(get_db)):
    """Display a single property's details."""
    property_obj = crud.get_property(db, property_id)
    if not property_obj:
        return RedirectResponse(url="/properties", status_code=303)
    return templates.TemplateResponse(
        "view_property.html", {"request": request, "property": property_obj}
    )


@app.get("/properties/{property_id}/edit", response_class=HTMLResponse)
def edit_property_form(property_id: int, request: Request, db: Session = Depends(get_db)):
    """Render a form pre-populated with an existing property's data."""
    property_obj = crud.get_property(db, property_id)
    if not property_obj:
        return RedirectResponse(url="/properties", status_code=303)
    return templates.TemplateResponse(
        "edit_property.html", {"request": request, "property": property_obj}
    )


@app.post("/properties/{property_id}/edit")
async def update_property(
    property_id: int, request: Request, db: Session = Depends(get_db)
):
    """Update an existing property and redirect to the list."""
    form = await request.form()
    data = {k: (v if v != "" else None) for k, v in dict(form).items()}
    if "has_mortgage" in data:
        data["has_mortgage"] = data["has_mortgage"] in {"yes", "true", "on", "1"}
    property_in = schemas.PropertyCreate(**data)
    crud.update_property(db, property_id, property_in)
    return RedirectResponse(url="/properties", status_code=303)


@app.post("/properties/{property_id}/delete")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    """Delete a property and redirect to the list."""
    crud.delete_property(db, property_id)
    return RedirectResponse(url="/properties", status_code=303)


# API endpoint for JSON-based property creation.
@app.post("/api/properties", response_model=schemas.Property, status_code=status.HTTP_201_CREATED)
def create_property_api(property_in: schemas.PropertyCreate, db: Session = Depends(get_db)):
    """Create a new property record from a JSON payload."""
    return crud.create_property(db, property_in)

# Include placeholder routers for future functionality.
app.include_router(stats.router)
app.include_router(refinancing.router)
app.include_router(acquisition.router)
