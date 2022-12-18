import sqlite3


class BotDB:

    def __init__(self, db_file):
        """Соединение с БД"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def address_old_exist(self, address):
        """Проверяем есть ли старый адрес в БД"""
        result = self.cursor.execute("SELECT address FROM photos_old WHERE address = ?", (address,))
        return bool(len(result.fetchall()))

    def address_new_exist(self, address):
        """Проверяем есть ли новый адрес в БД"""
        result = self.cursor.execute("SELECT address FROM photos_new WHERE address = ?", (address,))
        return bool(len(result.fetchall()))

    def get_link_old(self, address):
        """Получаем ссылки на фото из БД"""
        result = self.cursor.execute("SELECT link FROM photos_old WHERE address = ?", (address,))
        return result.fetchall()

    def get_link_new(self, address):
        """Получаем ссылки на фото из БД"""
        result = self.cursor.execute("SELECT link FROM photos_new WHERE address = ?", (address,))
        return result.fetchall()

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
