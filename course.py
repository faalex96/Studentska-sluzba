from professor import Professor, ProfessorSubject
from student import Student, Subject
import os

# Ispravke
# Razmisliti o godini na smeru, baza studenata po smeru/ali i po godini
# Napraviti bazu sa predmetima 
# Ispraviti format upisa studenta ako budem izvlacio nazad iz baze - split()
# Pre upisa bi trebalo napraviti index studentu i generisati ga automatski (da li student ili course)

class Course:
    # Razmisliti o godini na smeru.. 
    def __init__(self, course_title, course_professor):
        """ Initilize the title of the course and professor that represents it"""
        self.course_title = course_title
        self.course_professor = course_professor
        self.data_base_file = os.getcwd() + "\{} data.txt".format(self.course_title)        # Ovo treba srediti, nije dobar path
        with open(self.data_base_file, "w") as data_base:
            string_format = "*"*50 + " {} ".format(self.course_title) + "*"*50 + "\n\n"     
            data_base.write(string_format)

    def enroll_student(self, student):
        if student.course == self.course_title:
            with open(self.data_base_file, "a") as data_base:
                string_format = student.__str__() + "\n"                    
                data_base.write(string_format)
        print(self.data_base_file)

    def __str__(self):
        return "Course: {} Main Professor: {}".format(self.course_title, self.course_professor.full_name)

# Driver code
if __name__ == "__main__":
    # kreira profesora i smer
    prof = Professor("Nikola","Jorgovanovic","redovni profesor")
    biomedical_engineering = Course("Biomedical engineering", prof)

    # kreira studente
    Sale = Student("Aleksandar","Fa","aleksandarfa@devgmail.com", 1, "Biomedical engineering","budget")
    Marko = Student("Marko","Maric", "markomaric@gmail.com", 1, "Biomedical engineering", "personal")

    # upisi studente
    biomedical_engineering.enroll_student(Sale)
    biomedical_engineering.enroll_student(Marko)

    # ispis info o smeru
    print(biomedical_engineering)
    
