from datetime import datetime, date

class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age

    def send_to_database(self, cursor):
        query = "INSERT INTO employees (full_name, birth_date, gender) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.full_name, self.birth_date, self.gender))