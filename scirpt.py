from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from pynput.keyboard import Controller, Key
import asyncio
import time

# Define the TikTok username for the livestream
client = TikTokLiveClient(unique_id="@chatplaysgame")
keyboard = Controller()

# Modify the press_key function to handle multiple characters
def press_keys(input_keys):
    valid_keys = {
        "w": "w",
        "a": "a",
        "s": "s",
        "d": "d",
        "j": "j",
        "b": "b",
        "arial": "arial"
    }
    
    key_durations = {
        "w": 0.3,  
        "s": 0.3, 
        "a": 0.2, 
        "d": 0.2,  
        "j": 0.2, 
        "b": 0.2,
        "arial": 0.2
    }
    
    for char in input_keys:
        key_to_press = valid_keys.get(char)

        if key_to_press == "arial":
            arialBoost()
        elif key_to_press:
            print(f"Pressing '{key_to_press}' key")
            keyboard.press(key_to_press)
            time.sleep(key_durations.get(char, 0.3))  # Use the custom duration or default to 0.3
            keyboard.release(key_to_press)
        else:
            print(f"Ignored invalid command: {char}")

def arialBoost():
    #Jumping sequence
    print("Arial BOOST")
    keyboard.press(Key.space)
    time.sleep(0.1)
    keyboard.release(Key.space)

    #Tilting back
    keyboard.press(Key.s)
    time.sleep(0.2)
    keyboard.release(Key.s)

    #Boost Sequence
    keyboard.press(Key.b)
    time.sleep(0.3)
    keyboard.press(Key.b)


# Event listener for connection
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")

# Event listener for comments
async def on_comment(event: CommentEvent) -> None:
    message = event.comment.lower()
    print(f"{event.user.nickname} -> {message}")

    # Run press_keys in a separate thread to avoid blocking the async loop
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, press_keys, message)

# Add the on_comment listener manually
client.add_listener(CommentEvent, on_comment)

if __name__ == '__main__':
    client.run()
