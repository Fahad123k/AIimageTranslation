from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import io
from services.ocr_service import OCRService
from services.translation_service import translation_service
from routers.home_router import templates

router = APIRouter(tags=["OCR"])

@router.post("/translate/image", response_class=HTMLResponse)
async def translate_image(
    request: Request,
    target_lang: str = Form(...),
    image_file: UploadFile = File(...)
):
    try:
        if not image_file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Initialize OCR processor with target language
        ocr_processor = OCRService(target_lang=target_lang)
        
        image_bytes = io.BytesIO(await image_file.read())
        extracted_text = await ocr_processor.process_image(image_bytes)
        translated_text = await translation_service.translate_text(extracted_text, target_lang)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "original_text": extracted_text,
            "translated_text": translated_text,
            "target_lang": target_lang
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Processing error: {str(e)}"
        })