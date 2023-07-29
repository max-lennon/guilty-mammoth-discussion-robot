import os
import time
import pywikibot
from elevenlabs import generate, stream,set_api_key, voices, play, save
import vlc
import soundfile as sf
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

def read_message(message_text: str, use_streaming: bool = False):
    audio_output = generate(
        text=message_text,
        voice=ROBOT_VOICE,
        model="eleven_monolingual_v1",
        stream=use_streaming,
    )

    if use_streaming:
        stream(audio_output)
    else:
        discussion_tts = os.path.join(os.path.abspath(os.curdir), f"latest_discussion_topic.mp3")
        save(audio_output, discussion_tts)
        p = vlc.MediaPlayer(discussion_tts)
        p.play()
        wav_file = sf.SoundFile(discussion_tts)
        length_of_wav = wav_file.frames / wav_file.samplerate
        wav_file.close()
        time.sleep(length_of_wav + 1)
        p.stop()

    

def begin_discussion():
    message = "BEGIN DISCUSSION!"
    read_message(message)

def main():
    begin_discussion()

if __name__ == "__main__":
    main()
