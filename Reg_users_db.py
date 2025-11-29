#Библиотеки для хеширования и Базы Данных
import sqlite3
import hashlib

#Класс для рекурсий в Базе Данных
class UserDB:
    #Подключение к Базе Данных
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        self.placeholder = '?'

    #Создание таблицы пользователей
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) 
        """
        self.cursor.execute(query)
        self.conn.commit()

    #Регистрация нового пользователя
    def register_user(self, username, email, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            query = (f"INSERT INTO users (username, email, password_hash) VALUES ({self.placeholder}, {self.placeholder}, "
                     f"{self.placeholder})")
            self.cursor.execute(query, (username, email, password_hash))
            self.conn.commit()
            print("Пользователь успешно зарегистрирован.")
        except Exception as e:
            print(f"Ошибка регистрации: {e}")

    #Вход для старых пользователей
    def verify_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = f"SELECT password_hash FROM users WHERE username = {self.placeholder}"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result is None:
            print("Пользователь не найден.")
        stored_hash = result[0]
        if stored_hash == password_hash:
            print("Успешный вход!")
        else:
            print("Неверная пара логин-пароль.")

    #Все пользователи в приложении
    def list_all_users(self):
        print("Все пользователи: ")
        self.cursor.execute("SELECT username FROM users")
        users = self.cursor.fetchall()
        for user in users:
            print(user)


if __name__ == "__main__":
    db = UserDB()
    #Начало работы
    help_key = 0
    print("Добро пожаловать!")
    while help_key != 4:
        print("Выберите, какое действие вы хотели бы совершить:")
        print("1.Регистрация;")
        print("2.Вход;")
        print("3.Просмотр всех пользователей;")
        print("4.Выход")
        key_of_junction = int(input())
        help_key = key_of_junction
        if key_of_junction < 1 or key_of_junction > 4:
            print("Неверная команда.")
            while key_of_junction < 1 and key_of_junction > 4:
                key_of_junction = int(input())
                help_key = key_of_junction
        #Регистрация
        elif key_of_junction == 1:
            print("Хорошо, в следующих строчках напишите свои логин, почту и пароль (не забудьте его сохранить):")
            print("Логин: ")
            username = input()
            print("Почта: ")
            email = input()
            print("Пароль: ")
            password = input()
            db.register_user(username, email, password)
        #Вход для старых пользователей
        elif key_of_junction == 2:
            print("Хорошо, для входа введите логин и пароль:")
            print("Логин: ")
            username = input()
            print("Пароль: ")
            password = input()
            db.verify_user(username, password)
        #Просмотр всех пользователей
        elif key_of_junction == 3:
            db.list_all_users()
        #Выход
        else:
            print("Ну что же, увидимся позже!")