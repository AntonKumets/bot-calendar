import sqlite3

class Calendar:
    def __init__(self, db_name="holidays.db"):
        self.db_name = db_name

    def create_tables(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS holidays(
                month_id INTEGER PRIMARY KEY,
                holidays TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS season(
                month_id INTEGER PRIMARY KEY,
                season TEXT
            )
        """)

        con.commit()
        con.close()

    def fill_holidays(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        holidays = [
            (1, "Новый год(1 января), Рождество Христово (7 января), Старый Новый год (13-14 января)"),
            (2, "День защитника Отечества (23 февраля), Сретение Господне (15 февраля), День святого Валентина (14 февраля)"),
            (3, "Международный женский день (8 марта), Масленица (дата плавающая), Всемирный день театра (27 марта)"),
            (4, "Пасха(дата плавающая), День смеха (1 апреля), День космонавтики (12 апреля)"),
            (5, "Праздник Весны и Труда (1 мая), День Победы (9 мая), Международный день миротворцев ООН(25 мая)"),
            (6, "День России (12 июня), Троица (дата плавающая), День молодежи (27 июня)"),
            (7, "Иван Купала (7 июля), День семьи, любви и верности (8 июля), День Военно-морского флота (последнее воскресенье июля)"),
            (8, "День Воздушно-десантных войск (2 августа), День железнодорожника (3 августа), День кино (27 августа)"),
            (9, "День знаний (1 сентября), День программиста (13 сентября), День танкиста (Второе воскресенье сентября)"),
            (10, "Покров Пресвятой Богородицы (14 октября), День учителя (5 октября), Хэллоуин (31 октября)"),
            (11, "День народного единства (4 ноября), День матери (последнее воскресенье ноября), День морской пехоты (27 ноября)"),
            (12, "Новый год (31), День Конституции (12 декабря), Католическое Рождество (25 декабря)")
        ]

        cur.executemany("""
            INSERT OR IGNORE INTO holidays
            (month_id, holidays)
            VALUES (?, ?)
        """, holidays)

        con.commit()
        con.close()

    def fill_seasons(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        seasons = [
            (1, 'Зима'),
            (2, 'Зима'),
            (3, 'Весна'),
            (4, 'Весна'),
            (5, 'Весна'),
            (6, 'Лето'),
            (7, 'Лето'),
            (8, 'Лето'),
            (9, 'Осень'),
            (10, 'Осень'),
            (11, 'Осень'),
            (12, 'Зима')
        ]

        cur.executemany("""
            INSERT OR IGNORE INTO season
            (month_id, season)
            VALUES (?, ?)
        """, seasons)

        con.commit()
        con.close()

if __name__ == "__main__":
    db = Calendar("holidays.db")
    db.create_tables()
    db.fill_holidays()
    db.fill_seasons()