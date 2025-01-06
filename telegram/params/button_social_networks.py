from dataclasses import dataclass

from telegram.params.contacts_for_master_cb_data_message import confirm, change, remove


@dataclass
class SOCIAL_NETWORK:
    INSTAGRAM = ('Instagram', 'https://www.instagram.com/')
    TELEGRAM = ('Telegram', 'https://t.me/')
    VK = ('VK', 'https://vk.com/')
    FACEBOOK = ('Facebook', 'https://www.facebook.com/')
    OTHERS = 'Другие'


@dataclass
class SELECT_SOCIAL_NETWORK_CHANGE:
    USERNAME = 'Имя пользователя'
    SOCIAL_NETWORKS = 'Социальная сеть'


class PreviewSocialNetwork:
    def __init__(self, social_network: str, username: str):
        self.social_network = social_network
        self.username = username

    def generate_preview(self):
        return f'''Проверьте введенные данные:\n
- Социальная сеть:  {self.social_network}
- Ваше имя пользователя:  {self.username}\n\n
всё верно - нажмите «{confirm}»
нужно исправить - нажмите «{change}»'''

    def generate_preview_for_changes(self):
        return f'''Проверьте введенные данные:\n
- Социальная сеть:  {self.social_network}
- Ваше имя пользователя:  {self.username}'''

    def generate_preview_for_delete(self):
        return f'''Проверьте введенные данные:\n
- Социальная сеть:  {self.social_network}
- Ваше имя пользователя:  {self.username}'''
