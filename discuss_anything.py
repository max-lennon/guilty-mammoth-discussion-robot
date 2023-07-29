import pywikibot
from elevenlabs import generate, stream,set_api_key, voices, play, save
# import vlc
from AccessTokens import ELEVENLABS_API_KEY

# Set up ElevenLabs credentials
set_api_key(ELEVENLABS_API_KEY)

# Configurables
ROBOT_VOICE = "Mark 1 Discussion Bot"

voices_ = voices()
print(voices_)
# assert ROBOT_VOICE in voices_

def get_topic():
    pass

def read_message(message_text: str):
    audio_stream = generate(
        text=message_text,
        voice=ROBOT_VOICE,
        model="eleven_monolingual_v1",
        stream=True
    )
    stream(audio_stream)

def begin_discussion():
    message = "BEGIN DISCUSSION!"
    read_message(message)

def main():
    begin_discussion()

if __name__ == "__main__":
    main()
