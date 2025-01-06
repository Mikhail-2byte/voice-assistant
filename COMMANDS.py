from joke import tell_joke
from play_music import play_music
import random
import datetime
COMMANDS = {
    # Приветствие
    "привет как дела": lambda: random.choice([
        "Все хорошо, хозяин!",
        "Замечательно, а у вас?",
        "В полном порядке!",
        "Хорошо, спасибо, что спросили!"
    ]),
    

    # Представление
    "представься": lambda: random.choice([
        "Я слуга Михаила и служу ему!",
        "Меня зовут Настя, ваш голосовой помощник.",
        "Настя на связи, готова помочь."
    ]),
    
    # Уведомление о приходе хозяйки
    "хозяйка пришла домой": lambda: random.choice([
        "Ура, я очень рада!",
        "Здорово, всегда приятно, когда хозяйка дома!",
        "Добро пожаловать домой!"
    ]),
    
    # Время
    "сколько время": lambda: get_current_time(),
    
    # Шутка
    "расскажи шутку": lambda: tell_joke(),
    

    # Музыка
    "включи музыку": lambda: play_music(),
    "включи песню": lambda: play_music(),

    # Поиск в Википедии (добавляется отдельно в обработчике)
}

def get_current_time():
    """Возвращает текущее время."""
    now = datetime.datetime.now()
    return f"Сейчас {now.strftime('%H:%M:%S')}."

