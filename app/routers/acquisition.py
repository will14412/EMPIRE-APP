from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/acquisition", response_class=HTMLResponse)
async def read_acquisition(request: Request):
    """Placeholder page for acquisition operations."""
    return templates.TemplateResponse("acquisition.html", {"request": request})