import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Could not remove existing audio file: {e}")

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(text, func=lambda r=None: True):
    try:
        asyncio.run(TextToAudioFile(text))

        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            if func() is False:
                break
            clock.tick(10)

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

def TextToSpeech(text, func=lambda r=None: True):
    sentences = str(text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "You can see the rest of the text on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "Sir, check the chat screen for the rest of the text.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(sentences) > 4 and len(text) >= 250:
        intro = ". ".join(sentences[0:2]).strip() + "."
        outro = random.choice(responses)
        TTS(intro + " " + outro, func)
    else:
        TTS(text, func)

if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))
