from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import textwrap
import requests

import uvicorn

tags_metadata = [
    {
        "name": "Fake Trump Tweet",
        "description": "Send a GET request to ```https://faketrumptweets.herokuapp.com/tweet?text=```+your text.",
    }]

app = FastAPI(
	title="Fake Trump Tweets API",
    description="I needed an api of fake trump tweets for a meme but couldn't find it, so i made it.",
    version="1.0.5",
    docs_url=None, 
    redoc_url="/",
    openapi_tags=tags_metadata)

origins = [
	"https://harmz.xyz/",
	"https://www.harmz.xyz/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
)


@app.get("/tweet",response_class=FileResponse,tags=["Fake Trump Tweet"])
async def tweet(text: Optional[str]=None):
	try:
		img = Image.open("./blank.png")
	except Exception:
		blank = requests.get("https://firebasestorage.googleapis.com/v0/b/faketrumptweets-8c438.appspot.com/o/blank-2.png?alt=media&token=79366004-9c55-4c2b-b0aa-a970bf4c2b06")
		with open("blank.png","wb") as f:
			f.write(blank.content)
			f.close()
	img = Image.open("./blank.png")
	draw = ImageDraw.Draw(img)
	try:
		with open("font.ttf","rb") as font:
			font.close()
	except Exception:
		font = requests.get("https://firebasestorage.googleapis.com/v0/b/faketrumptweets-8c438.appspot.com/o/font.ttf?alt=media&token=9b1a1497-4284-4a3d-8212-91179f4720ea")
		with open('font.ttf', 'wb') as f:
			f.write(font.content)
			f.close()

	font = ImageFont.truetype("font.ttf", 18)
	lines = textwrap.wrap(text, width=60)
	if len(lines) > 1:
		draw.text((15, 62),"Maximum of 60 characters are allowed.",fill="#604af0",font=font)
	else:
		draw.text((15, 57),text,fill="#14171a",font=font)
	img.save("hi.png")
	file_like = open("./hi.png", mode="rb")
	return StreamingResponse(file_like, media_type="image/png")

