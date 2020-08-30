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

tags_metadata = [
    {
        "name": "Fake Trump Tweet",
        "description": "Send a GET request to ```https://faketrumptweets.herokuapp.com/tweet?text=```+your text.",
    }]

app = FastAPI(
	title="Fake Trump Tweets API",
    description="I needed an api of fake trump tweets for a meme but couldn't find it, so i made it.",
    version="1.0.0",
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
	#print(text)
	try:
		img = Image.open("./blank.png")
	except Exception:
		blank = requests.get("https://firebasestorage.googleapis.com/v0/b/faketrumptweets-8c438.appspot.com/o/blank.png?alt=media&token=dbecef3c-1e9e-478b-8c30-e78f225511c8")
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
	#print(font)
	lines = textwrap.wrap(text, width=60)
	#print(len(lines))
	#y_text = 90
	if len(lines) > 1:
		# for line in lines:
		#     width, height = font.getsize(line)
		#     draw.text(((15 + width) / 2, y_text), line, font=font, fill="#000")
		#     y_text += height
		#print("not supported")
		draw.text((15, 90),"Maximum of 60 characters are allowed.",fill="#000",font=font)
	else:
		draw.text((15, 85),text,fill="#000",font=font)
	img.save("hi.png")
	file_like = open("./hi.png", mode="rb")
	return StreamingResponse(file_like, media_type="image/png")