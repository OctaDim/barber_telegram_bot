import json

from aiogram.types import TelegramObject


def create_json_file_from_event(event: TelegramObject,
                                json_filename: str = "TestJSON.json") -> None:
    event_dict = event.model_dump(mode="json")

    with open(json_filename, "w") as json_file:
        json.dump(event_dict, json_file, indent=4, ensure_ascii=True)
