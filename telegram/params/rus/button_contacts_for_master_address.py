from telegram.params.contacts_for_master_cb_data_message import confirm, change
from telegram.parsing.generate_yandex_maps_link import MapsLinkBuilder


class PreviewAddress(MapsLinkBuilder):
    def __init__(self, address: str):
        super().__init__(address)
        self.address = address

    def generate_preview(self):

        url = self.get_link()
        preview_text = f'''
Проверьте введенные данные:\n
    - Ваш адрес:  <a href="{self.get_link()}">{self.address}</a>\n\n

Всё верно - нажмите «{confirm}». Нужно исправить - нажмите «{change}»'''

        return url, preview_text
