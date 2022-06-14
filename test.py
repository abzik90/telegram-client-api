import config
import asyncio
from telethon import TelegramClient, events
import PIL.Image

api_id = config.app_id
api_hash = config.app_hash

path = "C:/Users/Nurbol/Downloads/neko.jpg"

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]

def resize(image, new_width = 45):
    width, height = image.size
    new_height = int(new_width * height / width)
    return image.resize((new_width, new_height))

def to_greyscale(image):
    return image.convert("L")

def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "";
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25];
    return ascii_str

def asciify():
    global path
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "Unable to find image ")
    #resize image
    image = resize(image);
    #convert image to greyscale image
    greyscale_image = to_greyscale(image)
    # convert greyscale image to ascii characters
    ascii_str = pixel_to_ascii(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img=""
    #Split the string based on width  of the image
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    #save the string to a file
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_img);
    return ascii_img
async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    client.parse_mode = 'html'

    # print((await client.get_me()).stringify())
    await client.send_message('@yuhana369', 'Hello! Talking to you from Telethon')
    # await client.send_message(entity=entity,message=f"<code>{asciify()}</code>")
    await client.send_message('@yuhana369', f"<code>{asciify()}</code>")
    a = input()

asyncio.run(main())
