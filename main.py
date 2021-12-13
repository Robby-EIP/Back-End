from fastapi import FastAPI, File, UploadFile, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import aiofiles
from pydantic import BaseModel

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

def push_ino(file, robot):
    os.system('mv *.ino src/file.ino')
    ret = os.system('pio run -t upload')
    os.system('rm src/*.ino')
    if ret != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'File {file} could not be pushed to the robot {robot}')
    return 0

def cmds_to_file(cmds, robot_index):
    example = ""
    for i in cmds:
        l = i.split(' ')
        try:
            example += bloc_translate[robot_index][bloc_list[robot_index].index(l[0])] + "("
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unknown instruction {l[0]}')
        if len(l) > 1:
            for g in l[1:]:
                example += g + ','
            example = example[:len(example) - 1]
        example += ");"
    return example

def get_robot_index(robot):
    try:
        return(robots_index.index(robot))
    except:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
        detail=f'Robot {robot} type could not be recognized')





#Database preview
#Not Finished, fill robot_index with robots available, then fill other variables with pulls from github repos of robots
#Fill ips with dhcp protocol
robots_index = ['elegoo']
robots_ip = ["172.20.10.5:80"]
bloc_list = [['forward', 'back', 'left', 'right', 'wait']]
bloc_translate = [['forward', 'back', 'left', 'right', 'delay']]
bloc_args = [[0, 0, 0, 0, 1]]


#Work in assets folder for remote code push to the robot through platformio
os.chdir('./assets')




@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {'success': 'true', "string": "Hello World"}





class RawCode(BaseModel):
    code: str

@app.post('/push/rawcode', status_code=status.HTTP_200_OK)
def get_rawcode(robot: str, info: RawCode):
    get_robot_index(robot)
    f = open('./src/code.ino', "w")
    f.write(info.code)
    push_ino("code.ino", robot)
    return {'success': 'true', "detail": f'Code has been pushed to the robot', "robot": robot}





@app.post('/push/file', status_code=status.HTTP_200_OK)
async def push_file(robot: str, file: UploadFile = File(...)):
    async with aiofiles.open(f"./{file.filename}", 'wb+') as out_file:
        content = await file.read()
        await out_file.write(content)
    temp = file.filename.split('.')
    if temp[len(temp) - 1] == 'ino':
        push_ino(file.filename, robot)
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
        detail=f'File {file.filename} type could not be recognized')
    return {"success": "true", "detail": f'File {file.filename} has been pushed to the robot', "robot": robot}






class Blocs(BaseModel):
    setup: str
    loop: str

@app.post('/push/blocs', status_code=status.HTTP_200_OK)
def get_blocs(blocs: Blocs, robot: str):
    robot_index = get_robot_index(robot)
    f2 = open(f'../example/{robot}.ino', "r")
    example = f2.read()
    example += cmds_to_file(blocs.setup.split(','), robot_index)
    example += "}void loop(){" + cmds_to_file(blocs.loop.split(','), robot_index) + "}"
    f3 = open('./src/assets.ino', "w")
    f3.write(example)
    f3.close()
    push_ino("assets.ino", robot)
    return {'success': 'true'}






@app.get('/blocs', status_code=status.HTTP_200_OK)
def send_blocs(robot: str):
    try:
        robots_index.index(robot)
        return {"success": "true", "robot": "elegoo", "blocs": ','.join(bloc_list[robots_index.index(robot)])}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f'Robot {robot} not found in database')