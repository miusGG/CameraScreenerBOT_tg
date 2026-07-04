from dataclasses import dataclass
import json
from typing import List, Dict


@dataclass
class TgBot:
    token: str
    admins_ids: List[int]
    path_photo: str
    password: str

    @staticmethod
    def from_json(config: json):
        with open(config, 'r') as f:
            cfg = json.load(f)
        main_config = cfg['main']
        token = main_config['BOT_TOKEN']
        admin_ids = main_config['ADMINS']
        path_photo = main_config['path_photo']
        password = main_config['password']
        return TgBot(token=token, admins_ids=admin_ids, path_photo=path_photo, password=password)


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path):
    """
    :param path: .\cfg.json
    :return: 1 dataclass
    tg_bot:
        token
        admins_ids
        path_photo
        password
    """
    return Config(
        tg_bot=TgBot.from_json(path)
    )
