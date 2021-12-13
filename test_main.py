from fastapi.param_functions import Query
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


############################################################################
#                               HELLO WORLD


#hello world
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'success': 'true', "string": "Hello World"}




############################################################################
#                               PUSH RAWCODE

# No Robots Connected (elegoo)
def test_push_rawcode():
    response = client.post(
        "/push/rawcode",
        params={"robot": "elegoo"},
        json={"code": "empty"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": 'File code.ino could not be pushed to the robot elegoo'}

# Elegoo Connected and Good file
def test_push_rawcode():
    f = open("./test_files/elegoo_full.ino", "r")
    response = client.post(
        "/push/rawcode",
        params={"robot": "elegoo"},
        json={"code": f.read()},
    )
    assert response.status_code == 200
    assert response.json() == {'success': 'true', "detail": f'Code has been pushed to the robot', "robot": "elegoo"}


# Elegoo Connected and emptyfile
def test_push_rawcode():
    response = client.post(
        "/push/rawcode",
        params={"robot": "elegoo"},
        json={"code": ""},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": 'File code.ino could not be pushed to the robot elegoo'}




############################################################################
#                               PUSH FILE


def test_push_file():
    response = client.post(
        "/push/file",
        params={"robot": "elegoo"},
        files={"file": ("elegoo.ino", open("./../example/elegoo.ino", "rb"))}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": 'File elegoo.ino could not be pushed to the robot elegoo'}




############################################################################
#                               PUSH BLOCS


def test_push_blocs():
    response = client.post(
        "/push/blocs",
        params={"robot": "elegoo"},
        json={"setup": "forward,forward,back", "loop": "back"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": 'File assets.ino could not be pushed to the robot elegoo'}



############################################################################
#                               GET BLOCS

#elegoo
def test_get_blocs_elegoo():
    response = client.get(
        "/blocs",
        params={"robot": "elegoo"},
    )
    assert response.status_code == 200
    assert response.json() == {"success": "true", "robot": "elegoo",
    "blocs": "forward,back,left,right,wait"}

#wrong robot
def test_get_blocs_fail():
    response = client.get(
        "/blocs",
        params={"robot": "doesn't exist"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Robot doesn't exist not found in database"}