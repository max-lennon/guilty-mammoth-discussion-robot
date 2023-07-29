import os
import time
import random
from pywikibot import bot, pagegenerators, Site
from elevenlabs import generate, stream,set_api_key, voices, play, save
import vlc
import soundfile as sf
from AccessTokens import ELEVENLABS_API_KEY

# Set up ElevenLabs credentials
set_api_key(ELEVENLABS_API_KEY)

# Configurables go here
ROBOT_VOICE = "Mark 1 Discussion Bot"
tts_use_streaming = False # Whether to read TTS from a file or stream it
discussion_limit = 3 # If None, generates unlimited articles until program is halted. Set to an integer for a fixed number of discussions.
bot_min_wait = 30 # Shortest allowable time (in seconds) between discussion prompts
bot_max_wait = 300 # Longest allowable time (in seconds) between discussion prompts


# Mostly ripped from Doug's existing code, for compatibility and/or plagiarism reasons
def read_message(message_text: str):
    audio_output = generate(
        text=message_text,
        voice=ROBOT_VOICE,
        model="eleven_monolingual_v1",
        stream=tts_use_streaming,
    )

    if tts_use_streaming:
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

# Bot that continuously fetches new Wikipedia pages and does something with them
# 
# Page fetching behavior is defined by the page generator used to create the bot (in this case random articles)
class RandomDiscussionBot(bot.ExistingPageBot):
    
    def __init__(self, wait_time, **kwargs):
        super().__init__(**kwargs)
        self.min_wait_time, self.max_wait_time = wait_time
    
    # Can point this to other existing TTS functions if desired
    def read_page(self, text):
        print(text)
        return read_message(text)

    # This method defines the main behavior of the bot, i.e. what happens every time it accesses a new page.
    def treat_page(self):
        wait_time = random.randint(self.min_wait_time, self.max_wait_time)
        time.sleep(wait_time)    
        prompt_text = self.current_page.extract() # Summary section at the beginning of the article, sans formatting junk like links
        self.read_page(prompt_text + " BEGIN DISCUSSION!!!")


def create_bot():
    
    site = Site(url='https://en.wikipedia.org/wiki/')  # The site we want to run our bot on (in this case just English Wikipedia)

    rand_page_gen = pagegenerators.RandomPageGenerator(
        site=site,
        total=discussion_limit, # see explanation of discussion_limit in configurables section
        namespaces=[0], # namespace 0 corresponds to a standard article page (as opposed to talk pages, categories, etc.)
        )

    wiki_bot = RandomDiscussionBot(
        wait_time=(bot_min_wait, bot_max_wait),
        generator=rand_page_gen,
        )
    
    return wiki_bot

def main():
    discussion_bot = create_bot()
    discussion_bot.run()

if __name__ == "__main__":
    main()
