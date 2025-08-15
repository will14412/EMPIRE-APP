from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/refinancing", response_class=HTMLResponse)
async def read_refinancing(request: Request):
    """Placeholder page for refinancing operations."""
    return templates.TemplateResponse("refinancing.html", {"request": request})