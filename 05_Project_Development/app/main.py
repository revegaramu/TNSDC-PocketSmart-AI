import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.config import PROJECT_ROOT, settings
from app.database import (
    count_recommendations,
    create_user,
    get_db,
    get_recommendations,
    get_user_by_email,
    get_user_by_id,
    init_db,
    save_recommendation,
)
from app.schemas import (
    HomeRequest,
    JewelryRequest,
    LoginRequest,
    PartyRequest,
    RegisterRequest,
)
from app.security import (
    create_session_token,
    hash_password,
    verify_password,
)
from app.services.recommendations import (
    generate_image_aware_jewelry_recommendation,
    generate_recommendation,
)

TEMPLATE_DIR = PROJECT_ROOT / "app" / "templates"
STATIC_DIR = PROJECT_ROOT / "app" / "static"

app = FastAPI(
    title=settings.APP_NAME,
    description="Budget-aware AI planning and recommendation application",
    version="1.0.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="pocketsmart_session",
    same_site="lax",
    https_only=settings.SESSION_HTTPS_ONLY,
    max_age=60 * 60 * 24 * 7,
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.on_event("startup")
def startup() -> None:
    init_db()


def current_user(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    try:
        return get_user_by_id(int(user_id))
    except (ValueError, TypeError):
        request.session.clear()
        return None


def require_user(request: Request):
    user = current_user(request)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in to continue.",
        )

    return user


def page_context(request: Request, **extra: Any) -> dict[str, Any]:
    context = {
        "request": request,
        "app_name": settings.APP_NAME,
        "user": current_user(request),
    }
    context.update(extra)
    return context


def save_result(
    user_id: int,
    category: str,
    data: dict[str, Any],
    result: dict[str, Any],
) -> int:
    return save_recommendation(
        user_id=user_id,
        category=category,
        input_json=json.dumps(data, ensure_ascii=False),
        result_json=json.dumps(result, ensure_ascii=False),
    )


def generate_and_save(
    user,
    category: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    result = generate_recommendation(category, data)
    result_id = save_result(user["id"], category, data, result)
    result["id"] = result_id
    return result


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": settings.APP_NAME,
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    if current_user(request):
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=page_context(request),
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=page_context(request),
    )


@app.post("/register")
def register(data: RegisterRequest, request: Request):
    if get_user_by_email(data.email):
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    try:
        user_id = create_user(
            data.name,
            data.email,
            hash_password(data.password),
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    request.session.clear()
    request.session["user_id"] = user_id
    request.session["csrf_token"] = create_session_token()

    return {
        "message": "Account created successfully.",
        "user_id": user_id,
        "redirect": "/dashboard",
    }


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=page_context(request),
    )


@app.post("/login")
def login(data: LoginRequest, request: Request):
    user = get_user_by_email(data.email.strip())

    if not user or not verify_password(
        data.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password.",
        )

    request.session.clear()
    request.session["user_id"] = int(user["id"])
    request.session["csrf_token"] = create_session_token()

    return {
        "message": "Login successful.",
        "redirect": "/dashboard",
    }


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = current_user(request)

    if not user:
        return RedirectResponse("/login", status_code=303)

    history = get_recommendations(user["id"], limit=5)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=page_context(
            request,
            history=history,
            recommendation_count=count_recommendations(user["id"]),
        ),
    )


@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    if not current_user(request):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=page_context(request),
    )


@app.get("/party", response_class=HTMLResponse)
def party_page(request: Request):
    if not current_user(request):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context=page_context(request),
    )


@app.get("/jewelry", response_class=HTMLResponse)
def jewelry_page(request: Request):
    if not current_user(request):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context=page_context(request),
    )


@app.post("/generate-home")
def generate_home(data: HomeRequest, user=Depends(require_user)):
    result = generate_and_save(
        user,
        "home",
        data.model_dump(),
    )
    return result


@app.post("/generate-party")
def generate_party(data: PartyRequest, user=Depends(require_user)):
    result = generate_and_save(
        user,
        "party",
        data.model_dump(),
    )
    return result


@app.post("/generate-jewelry")
def generate_jewelry(data: JewelryRequest, user=Depends(require_user)):
    result = generate_and_save(
        user,
        "jewelry",
        data.model_dump(),
    )
    return result


@app.post("/recommendations-details")
def recommendation_details(
    recommendation_id: int = Form(...),
    user=Depends(require_user),
):
    with get_db() as db:
        row = db.execute(
            """
            SELECT id, category, input_json, result_json, created_at
            FROM recommendations
            WHERE id = ? AND user_id = ?
            """,
            (recommendation_id, user["id"]),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Not found.")

    return {
        "id": row["id"],
        "category": row["category"],
        "input": json.loads(row["input_json"]),
        "result": json.loads(row["result_json"]),
        "created_at": row["created_at"],
    }


@app.get("/history")
def history(user=Depends(require_user)):
    rows = get_recommendations(user["id"], limit=100)

    return [
        {
            "id": row["id"],
            "category": row["category"],
            "input": json.loads(row["input_json"]),
            "result": json.loads(row["result_json"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


@app.get("/session-info")
def session_info(user=Depends(require_user)):
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
    }


@app.get("/session-data")
def session_data(user=Depends(require_user)):
    return {
        "recommendation_count": count_recommendations(user["id"]),
    }


@app.post("/token")
def token(data: LoginRequest, request: Request):
    """
    Compatibility endpoint for clients expecting a token-style login.

    The application itself uses secure signed session cookies.
    """
    result = login(data, request)
    return {
        "access_token": "session-cookie",
        "token_type": "cookie",
        "redirect": result["redirect"],
    }


@app.post("/generate-jewelry-with-image")
async def generate_jewelry_with_image(
    occasion: str = Form(...),
    outfit_color: str = Form(...),
    budget: float = Form(...),
    jewelry_type: str = Form("Any"),
    notes: str = Form(""),
    image: UploadFile | None = File(None),
    user=Depends(require_user),
):
    data = JewelryRequest(
        occasion=occasion,
        outfit_color=outfit_color,
        budget=budget,
        jewelry_type=jewelry_type,
        notes=notes,
    ).model_dump()

    image_bytes = None
    mime_type = "image/jpeg"

    if image and image.filename:
        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Upload a JPEG, PNG, or WebP image.",
            )

        image_bytes = await image.read()

        max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
        if len(image_bytes) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"Image must be smaller than {settings.MAX_UPLOAD_MB} MB.",
            )

        mime_type = image.content_type or mime_type

    result = generate_image_aware_jewelry_recommendation(
        data,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )

    result_id = save_result(user["id"], "jewelry", data, result)
    result["id"] = result_id

    return result


@app.get("/startup")
def startup_status():
    return {
        "status": "ready",
        "database": "configured",
        "ai_configured": bool(settings.GEMINI_API_KEY),
    }


@app.get("/result/{recommendation_id}", response_class=HTMLResponse)
def result_page(recommendation_id: int, request: Request):
    user = current_user(request)

    if not user:
        return RedirectResponse("/login", status_code=303)

    with get_db() as db:
        row = db.execute(
            """
            SELECT id, category, input_json, result_json, created_at
            FROM recommendations
            WHERE id = ? AND user_id = ?
            """,
            (recommendation_id, user["id"]),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Result not found.")

    result = json.loads(row["result_json"])

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context=page_context(
            request,
            result=result,
            category=row["category"],
            created_at=row["created_at"],
        ),
    )