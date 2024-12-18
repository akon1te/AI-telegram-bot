from enum import Enum


class Action(Enum):
    WAIT_MESSAGE = 1
    IMG_GENERATION = 2
    TEXT_GENERATION = 3
    
    
TASK_TYPE_KEYBOARD = [
    ["Режим генерации картинок", "Режим диалога"],
]
TASK_SWITCH_TO_IMG_KEYBOARD = [
    ["Режим генерации картинок"],
]
TASK_SWITCH_TO_TEXT_KEYBOARD = [
    ["Режим диалога"],
]
