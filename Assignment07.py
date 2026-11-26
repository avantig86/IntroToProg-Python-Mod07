# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling.
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Avanti Gulhane,11/25/2026,Completed Assignment 07
# ------------------------------------------------------------------------------------------ #
import json

MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
'''
FILE_NAME: str = "Enrollments.json"
students: list = []
menu_choice: str = ""


class Person:
    """Represent a person with validated first and last names."""

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        """Get the first name."""
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        """Set a first name containing only alphabetic characters, or empty."""
        if not isinstance(value, str) or (value and not value.isalpha()):
            raise ValueError("First name must contain only letters.")
        self.__first_name = value

    @property
    def last_name(self) -> str:
        """Get the last name."""
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        """Set a last name containing only alphabetic characters, or empty."""
        if not isinstance(value, str) or (value and not value.isalpha()):
            raise ValueError("Last name must contain only letters.")
        self.__last_name = value

    def __str__(self) -> str:
        """Return the person's data as comma-separated text."""
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """Represent a student and their registered course; inherit from Person."""

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        """Get the registered course name."""
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        """Set a course name that is a string."""
        if not isinstance(value, str):
            raise ValueError("Course name must be text.")
        self.__course_name = value

    def __str__(self) -> str:
        """Return the student's name and course as comma-separated text."""
        return f"{super().__str__()},{self.course_name}"


class FileProcessor:
    """Provide static functions for loading and saving JSON student data."""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list = None) -> list:
        """Read dictionary rows from JSON and convert them to Student objects."""
        if student_data is None:
            student_data = []
        file = None
        try:
            file = open(file_name, "r", encoding="utf-8")
            json_students = json.load(file)
            for row in json_students:
                student_data.append(Student(row["FirstName"], row["LastName"], row["CourseName"]))
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with reading the file.", e)
        finally:
            if file is not None and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Convert Student objects to dictionaries and save them in JSON format."""
        file = None
        try:
            json_students = []
            for student in student_data:
                json_students.append({"FirstName": student.first_name,
                                      "LastName": student.last_name,
                                      "CourseName": student.course_name})
            file = open(file_name, "w", encoding="utf-8")
            json.dump(json_students, file, indent=4)
            print("Student registration data saved successfully.")
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with writing to the file.", e)
        finally:
            if file is not None and not file.closed:
                file.close()


class IO:
    """Provide static functions for user input, output, and error messages."""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Display a friendly error and optional technical details."""
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep="\n")

    @staticmethod
    def output_menu(menu: str):
        """Display the registration menu."""
        print("\n" + menu + "\n")

    @staticmethod
    def input_menu_choice() -> str:
        """Get and validate a menu choice from 1 to 4."""
        choice = ""
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise ValueError("Please choose only 1, 2, 3, or 4.")
        except Exception as e:
            IO.output_error_messages("Invalid menu choice.", e)
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """Display each Student object's comma-separated data."""
        print("-" * 50)
        for student in student_data:
            print(str(student))
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list) -> list:
        """Prompt for a student's details and append a validated Student object."""
        try:
            first_name = input("Enter the student's first name: ").strip()
            if not first_name or not first_name.isalpha():
                raise ValueError("First name must contain letters and cannot be empty.")
            last_name = input("Enter the student's last name: ").strip()
            if not last_name or not last_name.isalpha():
                raise ValueError("Last name must contain letters and cannot be empty.")
            course_name = input("Please enter the name of the course: ").strip()
            if not course_name:
                raise ValueError("Course name cannot be empty.")
            student = Student(first_name, last_name, course_name)
            student_data.append(student)
            print(f"\nYou have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with your entered data.", e)
        return student_data


if __name__ == "__main__":
    students = FileProcessor.read_data_from_file(FILE_NAME, students)
    while True:
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()
        if menu_choice == "1":
            students = IO.input_student_data(students)
        elif menu_choice == "2":
            IO.output_student_courses(students)
        elif menu_choice == "3":
            FileProcessor.write_data_to_file(FILE_NAME, students)
        elif menu_choice == "4":
            break
    print("Program Ended")
