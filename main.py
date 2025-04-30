from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode

app = FastAPI()

class QRRequest(BaseModel):
    imageUrl: str

@app.post("/decode")
def decode_qr(request: QRRequest):
    try:
        response = requests.get(request.imageUrl)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        result = decode(img)
        if not result:
            raise HTTPException(status_code=404, detail="QRコードが読み取れませんでした。")
        return { "url": result[0].data.decode("utf-8") }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"読み取りエラー: {str(e)}")
