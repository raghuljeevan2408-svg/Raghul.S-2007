from pathlib import Path
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.gemini_service import (
    home_recommendations,
    party_recommendations,
    jewelry_recommendations
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(
    title="PocketSmart AI"
)


# =====================================================
# STATIC FILES
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# =====================================================
# TEMPLATES
# =====================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# =====================================================
# HOME PAGE
# =====================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =====================================================
# TESTIMONIALS
# =====================================================

@app.get(
    "/testimonials",
    response_class=HTMLResponse
)
async def testimonials(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="testimonials.html"
    )


# =====================================================
# REGISTER PAGE
# =====================================================

@app.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


# =====================================================
# LOGIN PAGE
# =====================================================

@app.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# =====================================================
# LOGIN
# DEMO USER
# username = rax
# password = 123
# =====================================================

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):

    if username == "rax" and password == "123":

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return HTMLResponse(
        content="""
        <html>
        <head>
            <title>Login Failed</title>
        </head>

        <body>

            <h2>Invalid username or password</h2>

            <p>
                Demo username: rax
            </p>

            <p>
                Demo password: 123
            </p>

            <a href="/login">
                Back to Login
            </a>

        </body>
        </html>
        """,
        status_code=401
    )


# =====================================================
# USER DASHBOARD
# =====================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@app.get("/logout")
async def logout():

    return RedirectResponse(
        url="/login",
        status_code=303
    )

# =====================================================
# HOME PLANNER PAGE
# =====================================================

@app.get(
    "/home-planner",
    response_class=HTMLResponse
)
async def home_planner_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html"
    )
@app.post("/home-planner", response_class=HTMLResponse)
def generate_home_plan(
    request: Request,

    total_budget: float = Form(...),

    lights: int = Form(...),

    fans: int = Form(...),

    furniture: int = Form(...),

    dining_tables: int = Form(...),

    rooms: list[str] = Form(default=[]),

    requirements: str = Form("")
):

    room_text = ", ".join(rooms)

    requirements_text = f"""
Rooms: {room_text}

Number of Lights/Fixtures: {lights}

Number of Ceiling Fans: {fans}

Number of Furniture Pieces: {furniture}

Number of Dining Tables: {dining_tables}

Additional Requirements:
{requirements}
"""


    recommendations = home_recommendations(
        budget=total_budget,
        room=room_text,
        requirements=requirements_text
    )


    return templates.TemplateResponse(
        request=request,
        name="home_recommendations.html",
        context={
            "recommendations": recommendations
        }
    )
# =====================================================
# PARTY PLANNER PAGE
# =====================================================

@app.get("/party-planner")
def party_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html"
    )


@app.post("/party-planner", response_class=HTMLResponse)
def generate_party_plan(
    request: Request,
    budget: float = Form(...),
    guests: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(...),
    catering: str = Form(""),
    decoration: str = Form(""),
    entertainment: str = Form(""),
    requirements: str = Form("")
):

    recommendations = party_recommendations(
        budget=budget,
        guests=guests,
        event_type=event_type,
        venue=venue,
        catering=bool(catering),
        decoration=bool(decoration),
        entertainment=bool(entertainment),
        requirements=requirements
    )

    return templates.TemplateResponse(
        request=request,
        name="party_recommendations.html",
        context={
            "recommendations": recommendations
        }
    )

# =====================================================
# JEWELRY PLANNER PAGE
# =====================================================

# ============================================================
# JEWELRY PLANNER - PAGE
# ============================================================

@app.get("/jewelry-planner", response_class=HTMLResponse)
def jewelry_planner(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html"
    )


# ============================================================
# JEWELRY PLANNER - GENERATE RECOMMENDATIONS
# ============================================================

@app.post("/jewelry-planner", response_class=HTMLResponse)
async def generate_jewelry_plan(
    request: Request,

    total_budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(""),

    outfit_image: UploadFile = File(None)
):

    image_data = None
    mime_type = None

    if outfit_image and outfit_image.filename:

        image_data = await outfit_image.read()

        mime_type = (
            outfit_image.content_type
            or "image/jpeg"
        )

    recommendations = jewelry_recommendations(
        budget=total_budget,
        occasion=occasion,
        style=style,
        image_data=image_data,
        mime_type=mime_type
    )

    return templates.TemplateResponse(
        request=request,
        name="jewelry_recommendations.html",
        context={
            "recommendations": recommendations
        }
    )

# ============================================================

@app.get("/history", response_class=HTMLResponse)
def history(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="history.html"
    )