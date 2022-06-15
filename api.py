import config
import random
import flask
from flask import request

import asyncio
from telethon.sync import TelegramClient
from telethon import functions, types

api_id = config.app_id
api_hash = config.app_hash

client = TelegramClient('session_name', api_id, api_hash,)
# client.start()

async def connect_telethon():
    global client
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(config.default_phone)
        else:
            print("successfully logged in...")
        return True
    except Exception as e:
        print("Unable to connnect to Telethon...")
        print(e)
        return False

loop = asyncio.get_event_loop()
app = flask.Flask(__name__)

async def client_auth(auth_code):
    global client
    myself = await client.sign_in(config.default_phone, auth_code)

async def get_contact(phone_num):
    try:
        contact = await client.get_entity(phone_num)
        print("get_contact fired")
        return contact
    except:
        return False

def save_contact(phone_num):
    try:
        with TelegramClient("Telethon", api_id, api_hash) as client:
            result = client(functions.contacts.ImportContactsRequest(
                contacts=[types.InputPhoneContact(
                    client_id=random.randrange(-2**63, 2**63),
                    phone=phone_num,
                    first_name=phone_num,
                    last_name=''
                )]
            ))
            return True
    except:
            return False
        # return True
async def send_message(phone_num, message2send):
    entity=await get_contact(phone_num)
    if entity:
        await client.send_message(entity=entity,message=message2send)
        return True
    elif save_contact(phone_num):
        await send_message(phone_num, message2send)
    return False


@app.route('/',methods = ['GET'])
def home():
    phone_number = request.args['phone_number']
    message = request.args['message']
    # loop.run_until_complete(send_message(phone_number, message))
    if not loop.run_until_complete(send_message(phone_number, message)):
        return "{'success':false}"
    return "{'success':true}"
@app.route('/auth',methods = ['GET'])
def auth():
    auth_code = request.args['auth_code']
    if not loop.run_until_complete(client_auth(auth_code)):
        return "{'log_status':'something is wrong'}"
    return "{'log_status':'seems like nothing wrong'}"
@app.route('/connect',methods = ['GET'])
def connect_to():
    if not loop.run_until_complete(connect_telethon()):
        return "{'log_status':'something is wrong'}"
    return "{'log_status':'seems like nothing wrong'}"

if __name__ == '__main__':
    app.run(debug=True)

# ?phone_number=+77476722677&message=Hello%20from%20flask
