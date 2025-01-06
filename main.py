import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import datetime
import random
import wikipedia
import time
import sys
import pygame
from playsound import playsound
import os
from joke import tell_joke
from play_music import play_music
from COMMANDS import *

# Ключевые слова для активации
TRIGGER_WORD = "настя"
STOP_COMMAND = "остановись"

# Укажите индекс микрофона (проверьте список доступных микрофонов)
MICROPHONE_INDEX = 3  # Замените на ваш индекс



def speak(text, slow=False):
    """Озвучивает переданный текст с помощью gTTS."""
    tts = gTTS(text=text, lang='ru', slow=slow)
    tts.save("response.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)  # Ждем окончания воспроизведения
    pygame.mixer.quit()




def use_command(recognized_text):
    response = COMMANDS.get(recognized_text, None)
    if response:
        response_text = response()
    elif "википедия" in recognized_text:
        query = recognized_text.replace("википедия", "").strip()
        response_text = search_wikipedia(query)
    else:
        response_text = f"Команда не распознана: {recognized_text}"
    print(response_text)
    speak(response_text)


def search_wikipedia(query):
    """Ищет информацию на Wikipedia на русском языке."""
    try:
        wikipedia.set_lang("ru")
        if not query:
            return "Вы не указали, что искать в Википедии. Попробуйте снова."
        result = wikipedia.summary(query, sentences=2)
        return f"Вот что я нашела: {result}"
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])  # Показываем только первые 5 вариантов
        return f"Ваш запрос слишком общий. Возможно, вы имели в виду: {options}."
    except wikipedia.exceptions.PageError:
        return "Не удалось найти информацию по вашему запросу."
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Не удалось получить информацию с Wikipedia. Попробуйте позже."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

def listen_for_command():
    """Постоянно слушает и ждет ключевую команду."""
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
        print(f"Используется микрофон: {sr.Microphone.list_microphone_names()[MICROPHONE_INDEX]}")
        print("Ожидание команды...")
        while True:
            try:
                # Слушаем пользователя
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                command = recognizer.recognize_google(audio, language="ru-RU").lower()
                print(f"Распознанная команда: {command}")

                if TRIGGER_WORD in command:
                    print("Ключевое слово распознано! Жду следующую команду.")
                    soglasye = [
                        "Да, я слушаю",
                        "Да?",
                        "УГУ?",
                        "Слушаю?",
                        "Ваши указания?",
                        "Да, я тут.",
                        "Слушаю внимательно.",
                        "Что вы хотите?",
                        "Я здесь, говорите.",
                        "Что нужно?",
                        "Да.",
                        "Я тут.",       
                        "Говорите.",
                        "Что?",
                        "Я здесь.",
                        "Да-да.",
                        "Слушаю вас."                    
                    ]
                    speak(random.choice(soglasye))
                    listen_and_process_command()
                elif STOP_COMMAND in command:
                    print("Команда на завершение работы распознана. Отключаюсь.")
                    speak("Выключаюсь. До свидания!")
                    sys.exit()  # Завершаем выполнение программы

            except sr.UnknownValueError:
                print("Не удалось распознать. Попробуйте снова.")
            except sr.RequestError as e:
                print(f"Ошибка запроса к сервису Google Speech Recognition: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

def listen_and_process_command():
    """Слушает пользователя и передает команду на обработку."""
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
        print("Говорите вашу команду:")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            recognized_text = recognizer.recognize_google(audio, language="ru-RU").lower()
            print(f"Распознанный текст: {recognized_text}")

            # Передаем текст в обработчик команд
            use_command(recognized_text)

        except sr.UnknownValueError:
            print("Не удалось распознать текст. Попробуйте снова.")
            speak("Не удалось распознать текст. Попробуйте снова.")
        except sr.RequestError as e:
            print(f"Ошибка запроса к сервису Google Speech Recognition: {e}")
            speak("Произошла ошибка подключения к сервису распознавания.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            speak("Произошла ошибка.")

if __name__ == "__main__":
    print("Доступные микрофоны:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")

    listen_for_command()
