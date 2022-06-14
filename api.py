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
client.start()

loop = asyncio.get_event_loop()
app = flask.Flask(__name__)

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
    loop.run_until_complete(send_message(phone_number, message))

    return "{'success':true}"

if __name__ == '__main__':
    app.run()
# ?phone_number=+77476722677&message=Hello%20from%20flask
