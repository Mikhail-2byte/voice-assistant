import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import datetime
import random
import wikipedia
import time
import sys

from joke import tell_joke


# Ключевые слова для активации
TRIGGER_WORD = "настя"
STOP_COMMAND = "остановись"

import pygame

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
    """Обрабатывает команды после распознавания текста."""
    if recognized_text == "привет как дела":
        response = "Все хорошо, хозяин!"
        print(response)
        speak(response)
    elif recognized_text == "включи свет":
        response = "Включаю свет"
        print(response)
        speak(response)
    elif recognized_text == "выключи свет":
        response = "Выключаю свет"
        print(response)
        speak(response)
    elif recognized_text == "представься":
        response = "Я слуга Михаила и служу ему!"
        print(response)
        speak(response)
    elif recognized_text == "хозяйка пришла домой":
        response = "Ура, я очень рада!"
        print(response)
        speak(response)
    elif recognized_text == "какое сейчас время" or recognized_text == "сколько время":
        response = get_current_time()
        print(response)
        speak(response)
    elif recognized_text == "скажи шутку" or recognized_text == "расскажи шутку":
        response = tell_joke()
        print(response)
        speak(response)
    elif "википедия" in recognized_text:
        query = recognized_text.replace("википедия", "").strip()
        response = search_wikipedia(query)
        print(response)
        speak(response)
    else:
        response = f"Команда не распознана: {recognized_text}"
        print(response)
        speak(response)

def get_current_time():
    """Возвращает текущее время."""
    now = datetime.datetime.now()
    return f"Сейчас {now.strftime('%H:%M:%S')}."

def search_wikipedia(query):
    """Ищет информацию на Wikipedia на русском языке."""
    try:
        wikipedia.set_lang("ru")
        if not query:
            return "Вы не указали, что искать в Википедии. Попробуйте снова."
        result = wikipedia.summary(query, sentences=2)
        return f"Вот что я нашел: {result}"
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
    with sr.Microphone() as source:
        print("Ожидание команды...")
        while True:
            try:
                # Слушаем пользователя
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                command = recognizer.recognize_google(audio, language="ru-RU").lower()
                print(f"Распознанная команда: {command}")

                if TRIGGER_WORD in command:
                    print("Ключевое слово распознано! Жду следующую команду.")
                    speak("Да, я слушаю")
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
    with sr.Microphone() as source:
        print("Говорите вашу команду:")
        try:
            # Слушаем пользователя
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
    listen_for_command()
