import re
import urllib.request
import os
from urllib.error import URLError
from PIL import Image
from src.config import url
from src.data_store import data_store
from src.error import InputError, AccessError



def user_details(u_id):
    store = data_store.get()
    
    if u_id not in store['user_details'].keys():
        raise InputError("The u_id provided doesn't exist")
    
    user = store['user_details'].get(u_id)
    
    return {
        'u_id' : u_id,
        'email' : user[0],
        'name_first' : user[2],
        'name_last' : user[3],
        'handle_str' : user[4],
        'profile_img_url' : user[5]
    }

def list_all_users():
    store = data_store.get()
    users = []
    
    for u_id, user in store['user_details'].items():
        if user[0] == "" and user[4] == "" and user[2] == 'Removed' and user[3] == 'user':
            continue
        else:
            users.append({
                'u_id' : u_id,
                'email' : user[0],
                'name_first' : user[2],
                'name_last' : user[3],
                'handle_str' : user[4],
                'profile_img_url' : user[5]
            })
    
    return users


def user_set_name(u_id, name_first, name_last):
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("First name must be between 1 and 50 characters")
    elif len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Last name must be between 1 and 50 characters")
        
    store = data_store.get()
    
    user = list(store['user_details'].get(u_id))
    user[2] = name_first
    user[3] = name_last
    
    user = tuple(user)
    store['user_details'].update({u_id: user})

def user_set_email(u_id, email):
    #implement error for email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) is None:
        raise InputError("Non-valid email format!")
    
    store = data_store.get()
    
    #implement error checking for duplicate
    if email in store['registered_users'].keys():
        raise InputError("A user with that email already exists")

    user = list(store['user_details'].get(u_id))
    user[0] = email
    
    user = tuple(user)
    store['user_details'].update({u_id: user})

def user_set_handle(u_id, handle_str):
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle length must be between 3 to 20 characters")
    elif handle_str.isalnum() == False:
        raise InputError("Handle contains non-alphanumeric characters")
     
    store = data_store.get()
    
    for user_id, usr in store['user_details'].items():
        if user_id != u_id and usr[4] == handle_str:
            raise InputError("Handle is taken by another user")
    
    user = list(store['user_details'].get(u_id))
    user[4] = handle_str
    
    user = tuple(user)
    
    store['user_details'].update({u_id: user})
    
    
def user_profile_uploadphoto(user_id, img_url, x_start, y_start, x_end, y_end):
    store = data_store.get()
    
    user = store['user_details'].get(user_id)
    u_handle = user[4]
    
    path = u_handle + ".jpg"
    
    # x_start, y_start, x_end, y_end are negative
    if x_start < 0 or y_start < 0 or x_end < 0 or y_end < 0:
          raise InputError("Invalid crop dimensions")     
          
    # if x_start >= x_end 
    if x_end < x_start:
        raise InputError("Invalid crop dimensions")
        
    # if y_start >= y_end
    if y_end < y_start:
        raise InputError("Invalid crop dimensions")

    try:
        urllib.request.urlretrieve(img_url, "src/static/" + path)
    except (URLError, ValueError):
        raise InputError("Invalid image url passed") from None
         
    imageObject = Image.open("src/static/" + path)
    
    if imageObject.format != 'JPEG':
        os.remove("src/static/" + path)
        raise InputError("Image format must be a JPEG/JPG")
    
    # Dimensions Error Cases
    width, height = imageObject.size
    
    # if y_start or y_end >= height
    if y_start > height or y_end > height:
        os.remove("src/static/" + path)
        raise InputError("Invalid crop dimensions")
        
    # if x_start or x_end >= width
    if x_start > width or x_end > width:
        os.remove("src/static/" + path)
        raise InputError("Invalid crop dimensions")
    
    cropped_image = imageObject.crop((x_start, y_start, x_end, y_end))
    
    cropped_image.save("src/static/" + path)
    
    new_img_url = url + "src/static/" + path
    
    store['user_details'].update({user_id : (user[0], user[1], user[2], user[3], user[4] , new_img_url)})
    
def user_stats_v1(u_id):
    store = data_store.get()
    
    #(sum(num_channels_joined, num_dms_joined, num_msgs_sent)) / (sum(num_channels, num_dms, num_msgs))
    #If denominator = 0 then involvement = 0, involvement capped at 1.
    #Denominator
    num_channels = len(store['channels'])
    num_dms = len(store['dms'])
    num_msgs = len(store['messages']) + len(store['standups'])


    denominator = num_channels + num_dms + num_msgs

    #Numerator
    channels = store['user_stats'][u_id]['channels_joined']
    num_channels_joined = channels[-1]['num_channels_joined']

    dms = store['user_stats'][u_id]['dms_joined']
    num_dms_joined = dms[-1]['num_dms_joined']

    msgs = store['user_stats'][u_id]['messages_sent']
    num_msgs_sent = msgs[-1]['num_messages_sent']

    numerator = num_channels_joined + num_dms_joined + num_msgs_sent

    #Involvement
    if denominator == 0:
        involvement = 0.0
    else:
        involvement = numerator / denominator
    
    if involvement > 1:
        involvement = 1.0
    
    user_stats = store['user_stats'][u_id]
    user_stats.update({'involvement_rate' : involvement})

    return user_stats
