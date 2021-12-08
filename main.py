from typing import Optional

from fastapi import FastAPI, Body, Request, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
#from starlette.responses import aiofiles
import os
import time
import aiofiles

testvar:int = 0

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "https://127.0.0.1:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class TestItem(BaseModel):
    code: str

def push_ino():
    os.system('mv *.ino src/file.ino')
    os.system('pio run -t upload')
    os.system('rm src/*.ino')

def push_hex():
    os.system('mv *.hex assets.hex')
    os.system('pio run -t upload')
    os.system('rm *.hex')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/push/rawcode')
def get_rawcode(test: TestItem):
    f = open('./assets/code.ino', "w")
    f.write(test.code)
    return {'success': 'true'}

@app.post('/push/executable')
async def image(file: UploadFile = File(...)):
    print(file)
    os.chdir('./assets')
    async with aiofiles.open(f"./{file.filename}", 'wb+') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    temp = file.filename.split('.')
    if temp[len(temp) - 1] == 'hex':
        push_hex()
    elif temp[len(temp) - 1] == 'ino':
        push_ino()
    os.chdir('..')
    return {"success": "true"}

@app.post('/push/blocs')
def get_blocs(test: TestItem):
    os.chdir('./assets')
    f = open('./code' + '.bloc', "w")
    f.write(test.code)
    cmds = test.code.split(',')
    print(cmds)
    f2 = open('../example/starter.ino', "r")
    example = f2.read()
    example += '\n\nvoid loop() {\n'
    for i in cmds:
        if i == 'forward':
            example += 'forward()'
        elif i == 'right':
            example += 'right()'
        elif i == 'left':
            example += 'left()'
        elif i == 'back':
            example += 'back()'
        elif i.find('delay') != -1:
            example += i
        example += ';\n'
    example += '}'
    f3 = open('./assets.ino', "w")
    f3.write(example)
    f3.close()
    push_ino()
    os.system('rm code.bloc')
    os.chdir('..')
    return {'success': 'true'}