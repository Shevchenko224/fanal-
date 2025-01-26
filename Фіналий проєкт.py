import sqlite3
import requests
from bs4 import BeautifulSoup


class DatabaseManager:
    def __init__(self, db_path="links.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL
        )
        """)
        connection.commit()
        connection.close()

    def add_link(self, url):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO links (url) VALUES (?)", (url,))
        connection.commit()
        connection.close()

    def get_links(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT url FROM links")
        links = [row[0] for row in cursor.fetchall()]
        connection.close()
        return links


class WebParser:
    def fetch_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Помилка при завантаженні {url}: {e}")
            return None

    def parse_table(self, html_content, keyword):
        soup = BeautifulSoup(html_content, features="html.parser")
        table = soup.find('table')  # Уточніть атрибут таблиці, якщо необхідно
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:
                columns = row.find_all('td')
                if len(columns) > 2:
                    name = columns[2].text.strip()
                    price = columns[3].text.strip()
                    if keyword.lower() in name.lower():
                        return f"{name}: {price}"
        return None


class UserInterface:
    @staticmethod
    def display_message(message):
        print(message)

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)


class MainApplication:
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.web_parser = WebParser()
        self.user_interface = UserInterface()

    def run(self):
        while True:
            self

