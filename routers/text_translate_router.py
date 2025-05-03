from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from services.translation_service import translation_service
from routers.home_router import templates

router = APIRouter(tags=["Translation"])

@router.post("/translate/text", response_class=HTMLResponse)
async def translate_text(
    request: Request,
    text: str = Form(...),
    target_lang: str = Form(...)
):
    try:
        translated_text = await translation_service.translate_text(text, target_lang)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "original_text": text,
            "translated_text": translated_text,
            "target_lang": target_lang
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Translation error: {str(e)}"
        })