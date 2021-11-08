import pytest
from urllib.error import URLError
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import upload_photo
from wrapper.clear_wrapper import clear_http
from src.user import user_profile_uploadphoto

ACCESS_ERROR = 403
INPUT_ERROR = 400

# This is a JPG image of dimensions 750 x 1000
IMAGE_URL = "https://i.pinimg.com/originals/22/b7/3d/22b73ddfc4cbe22a4a6a4799bb37488b.jpg"

# PNG image should not work
PNG_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
  
def test_negatives_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, IMAGE_URL, -1, -1, 50, 50)
    assert r1.status_code == INPUT_ERROR
    
    
def test_x_start_gt_end_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, IMAGE_URL, 300, 600, 150, 600)
    assert r1.status_code == INPUT_ERROR
    
def test_y_start_gt_end_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, IMAGE_URL, 150, 600, 150, 300)
    assert r1.status_code == INPUT_ERROR
    
def test_y_gt_height_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, IMAGE_URL, 150, 1001, 300, 1200)
    assert r1.status_code == INPUT_ERROR
    
    
def test_x_gt_width_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, IMAGE_URL, 751, 500, 800, 600)
    assert r1.status_code == INPUT_ERROR

def test_not_jpg_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']  
    
    r1 = upload_photo(token, PNG_IMAGE, 0, 0, 300, 300)
    assert r1.status_code == INPUT_ERROR
    
def test_invalid_url_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, 'thisisnotreal.cool.au' , 0, 0, 500, 800)
    assert r1.status_code == INPUT_ERROR
    
def test_basic_uploadphoto():
    clear_http()
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r.json()['token']
    
    r1 = upload_photo(token, IMAGE_URL, 0, 0, 500, 800)
    assert r1.json() == {}


