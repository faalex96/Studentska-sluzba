from professor import Professor, ProfessorSubject
from student import Student
from subject import Assignment, Subject
from datetime import datetime
import os

class Course:
    def __init__(self, course_title, students_num, course_professor):

        """ Initilize the title of the course and professor that represents it"""
        self.course_title = course_title
        self.course_professor = course_professor
        self.__course_generation = datetime.now().year
        self.student_data_base = os.getcwd() + "\{}_{}_data.txt".format(self.course_title, self.__course_generation)
        self.subject_data_base = "{}_subjects_data.txt".format(self.course_title)
        self.__student_index = 1
        self.students_num = students_num
        

        # Create datebase when course is created
        with open(self.student_data_base, "w") as data_base:
            string_format = "*"*50 + " {} {}".format(self.course_title, self.__course_generation) + "*"*50 + "\n\n"     
            data_base.write(string_format)

    def enroll_student(self, student):
        """Checks if the course capacity is not full. Generates students index_number. Add student to his datebase."""
        if self.__student_index <= self.students_num:
            if student.course == self.course_title:
                student.index_number =  "{}{}-{}".format(self.course_acronym, self.__student_index, str(self.__course_generation))    
                self.__student_index += 1

                # Add student to database
                with open(self.student_data_base, "a") as data_base:
                    string_format = "{}, {}\n".format(student.index_number, student.__str__())                    
                    data_base.write(string_format)
        else:
            print("Course capacity full.")

    @property
    def course_acronym(self):
        """Generates course acronym based on courses first letters in title. """
        acronym = self.course_title.split(" ")
        ac = "".join(list(map(lambda word: word[0].upper(), acronym)))
        return ac

    def create_subject_database(self):
        """ Creates a subject database """
        with open(self.subject_data_base, "w") as subjects_data:
            subjects_data.write("*"*50 + self.course_title + "*"*50 + "\n\n")

    def add_subjects(self, *subjects):
        """ Adds ProfessorSubject to subjects of course """
        with open(self.subject_data_base, "a") as subject_data:
            for sub in subjects:
                string_format = sub.__str__() + "\n"
                subject_data.write(string_format)

    def __str__(self):
        return "Course: {} Main Professor: {}".format(self.course_title, self.course_professor.full_name)

# Driver code
if __name__ == "__main__":
    # kreira profesora i smer
    prof = Professor("Nikola","Jorgovanovic","redovni profesor")
    biomedical_engineering = Course("Biomedical engineering", 60, prof)

    # kreira studente
    Sale = Student("Aleksandar","Fa","aleksandarfa@devgmail.com", 1, "Biomedical engineering","budget")
    Marko = Student("Marko","Maric", "markomaric@gmail.com", 1, "Biomedical engineering", "personal")

    # upisi studente
    biomedical_engineering.enroll_student(Sale)
    biomedical_engineering.enroll_student(Marko)

    # Dodaj predmete sa profesorima u bazu
    Spasic = Professor("Dragan","Spasic", "redovni profesor")
    Okuka = Professor("Aleksandar","Okuka", "asistent")

    mehanika = ProfessorSubject("Mehanika", "101", 9)
    mehanika.add_professors(Spasic, Okuka)
    a = Assignment("Statika", datetime(2021, 1, 30))
    mehanika.add_assignements(a)
    mehanika.print_assignements()
    
    Segedinac = Professor("Milan","Segedinac", "redovni profesor")
    racunarstvo = ProfessorSubject("Racunarstvo", "102", 12)
    racunarstvo.add_professors(Segedinac)

    biomedical_engineering.create_subject_database()
    biomedical_engineering.add_subjects(mehanika, racunarstvo)


    
