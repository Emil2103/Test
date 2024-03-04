import sys
import class_DB

if __name__ == "__main__":

    mode = int(sys.argv[1])

    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    database = "ptmk_test"

    directory = class_DB.EmployeeDirectory(host, port, user, password, database)

    if mode == 1:

        directory.create_employee_table()
        directory.close_connection()

    elif mode == 2:
        if len(sys.argv) != 5:
            print("Usage: python myApp.py 2 <full_name> <birth_date> <gender>")
            sys.exit(1)

        full_name = sys.argv[2]
        birth_date = sys.argv[3]
        gender = sys.argv[4]

        directory.add_employee(full_name, birth_date, gender)
        directory.close_connection()

    elif mode == 3:
        directory.retrieve_employees()
        directory.close_connection()

    elif mode == 4:
        directory.add_employees_bulk(directory.generate_employees(1000000))
        directory.add_employees_with_specific_criteria(100, 'Male', 'F')
        directory.close_connection()

    elif mode == 5:
        directory.selection_by_condition('Male', 'F')
        directory.close_connection()

    elif mode == 6:
        # Индексы в базе данных - это структуры данных, создаваемые для ускорения поиска и фильтрации данных.
        directory.optimize_database()
        directory.selection_by_condition('Male', 'F')
        directory.close_connection()
    elif mode == 7:
        directory.delete_table()
        directory.close_connection()
    else:
        print("Invalid mode. Available modes: 1 (create table), 2 (add employee), 3 (show employees),"
              "4 (add employees), 5 (search query), 6 (optimized search query), 7 (delete table)")

