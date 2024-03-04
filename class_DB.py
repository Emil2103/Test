import pymysql
import class_Employee
from datetime import datetime, timedelta
import random
import string
import time

class EmployeeDirectory:
    def __init__(self, host, port, user, password, database):
        try:
            self.connection = pymysql.connect(
                host = host,
                port = port,
                user = user,
                password = password,
                database = database,
            )
            self.cursor = self.connection.cursor()
            print("successfully connected...")
            print("#" * 20)

        except Exception as ex:
            print("Connection refused...")
            print(ex)

    def create_employee_table(self):
        query = "CREATE TABLE IF NOT EXISTS employees ("\
            "id INT AUTO_INCREMENT PRIMARY KEY,"\
            "full_name VARCHAR(255),"\
            "birth_date DATE,"\
            "gender ENUM('Male', 'Female'));"

        self.cursor.execute(query)
        self.connection.commit()
        print("Employee table created successfully")

    def add_employee(self, full_name, birth_date, gender):
        employee = class_Employee.Employee(full_name, birth_date, gender)
        employee.send_to_database(self.cursor)
        self.connection.commit()
        print("Employee added successfully")

    def retrieve_employees(self):
        query = "SELECT DISTINCT full_name, birth_date, gender FROM employees ORDER BY full_name"
        self.cursor.execute(query)
        employees = self.cursor.fetchall()
        for employee in employees:
            full_name = employee[0]
            birth_date = employee[1]
            gender = employee[2]
            employee_obj = class_Employee.Employee(full_name, birth_date, gender)
            age = employee_obj.calculate_age()
            print(f"Full Name: {full_name}, Birth Date: {birth_date}, Gender: {gender}, Age: {age}")

    def add_employees_bulk(self, data):
        query = "INSERT INTO employees (full_name, birth_date, gender) VALUES (%s, %s, %s)"
        self.cursor.executemany(query, data)
        self.connection.commit()

    def generate_random_name(self):
        letters = string.ascii_letters
        first_name = ''.join(random.choice(letters).lower() for i in range(8)).capitalize()
        last_name = ''.join(random.choice(letters).lower() for i in range(8)).capitalize()
        patronymic = ''.join(random.choice(letters).lower() for i in range(8)).capitalize()
        return f"{last_name} {first_name} {patronymic}"

    def generate_random_date(self, start_date, end_date):
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days)
        return random_date

    def generate_random_gender(self):
        return random.choice(['Male', 'Female'])

    def generate_employees(self, count):
        employees = []
        gender_counts = {'Male': 0, 'Female': 0}
        surname_counts = {letter: 0 for letter in
                          string.ascii_uppercase}  # Словарь для отслеживания количества имен по первой букве фамилии
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2000, 1, 1)

        while len(employees) < count:
            gender = self.generate_random_gender()
            full_name = self.generate_random_name()
            first_letter = full_name.split()[0][0].upper()  # Получаем первую букву фамилии
            birth_date = self.generate_random_date(start_date, end_date)

            # Проверяем количество имен для данной первой буквы фамилии
            if surname_counts[first_letter] < count / len(string.ascii_uppercase):
                employees.append((full_name, birth_date, gender))
                gender_counts[gender] += 1
                surname_counts[first_letter] += 1

        return employees


    def add_employees_with_specific_criteria(self, count, gender, surname_start):
        employees = []
        for _ in range(count):
            full_name = surname_start + self.generate_random_name()[1:]
            birth_date = self.generate_random_date(datetime(1950, 1, 1), datetime(2000, 1, 1))
            employees.append((full_name, birth_date, gender))
        self.add_employees_bulk(employees)

    def selection_by_condition(self, get_gender, first_letter_lastname):
        start_time = time.time()
        query = "SELECT gender, full_name FROM employees" \
                " WHERE gender = %s and full_name LIKE %s"
        self.cursor.execute(query, (get_gender, first_letter_lastname + "%"))
        end_time = time.time()
        # employees = self.cursor.fetchall()
        # for employee in employees:
        #     full_name = employee['full_name']
        #     gender = employee['gender']
        #     print(f"Full Name: {full_name}, Gender: {gender}")
        execution_time = end_time - start_time
        print(f"Query executed in {execution_time} seconds")

    def optimize_database(self):
        try:
            self.cursor.execute("CREATE INDEX idx_gender ON employees(gender)")
            self.cursor.execute("CREATE INDEX idx_full_name ON employees(full_name)")
            print("Indexes created successfully")
        except Exception as e:
            print(f"Error creating indexes: {str(e)}")


    def delete_table(self):
        query = "DROP TABLE employees"
        self.cursor.execute(query)
        self.connection.commit()
        print("Table was delete")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()