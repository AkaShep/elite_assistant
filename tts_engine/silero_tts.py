# tts_engine/silero_tts.py
import torch
import sounddevice as sd
import numpy as np
import time
from num2words import num2words
import re

model = None
speaker = None
sample_rate = None
device = None

def init_tts(config):
    global model, speaker, sample_rate
    language = config.get("voice_language", "ru")
    model_id = config.get("model_id", "v4_ru")
    sample_rate = config.get("sample_rate", 48000)
    speaker = config.get("default_speaker", "xenia")
    device = torch.device('cpu')

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
    model.to(device)

def replace_numbers_with_words(example_text, lang='ru'):
    def replace(match):
        number = match.group()
        return num2words(number, lang=lang)
    # Заменяем все целые и дробные числа
    return re.sub(r'\d+(\.\d+)?', replace, example_text)    

def speak(example_text):   
    if model is None:
        print("[TTS] Ошибка: модель не загружена")
        return
    
    example_text = replace_numbers_with_words(example_text)

    audio = model.apply_tts(
        text=example_text,
        speaker= speaker,
        sample_rate= sample_rate
    )

    
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate)
    sd.stop()