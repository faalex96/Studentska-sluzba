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

    
    def serilize_dict(self,d, delim=";"):
        string = ""
        for i, key in enumerate(d):
            

            if isinstance(d[key], list):
                string += str(key)+ ":" + self.serilize_list(d[key])
            else:
                string += str(key) + ":" + str(d[key])

            if i != len(d)-1:
                string += delim
                
        return string 

    
    def serilize_list(self,lst):
        string = "["
        for i, obj in enumerate(lst):
            temp_dict = obj.__dict__
            string += self.serilize_dict(temp_dict, "/")
            if i != len(lst)-1:
                string  += ","
            
        return string + "]"


    def enroll_student(self, student):
        """Checks if the course capacity is not full. Generates students index_number. Add student to his datebase."""
        if self.__student_index <= self.students_num:
            if student.course == self.course_title:
                student.index_number =  "{}{}-{}".format(self.course_acronym, self.__student_index, str(self.__course_generation))    
                self.__student_index += 1
                string_format = self.serilize_dict(student.__dict__)

                # Add student to database
                with open(self.student_data_base, "a") as data_base:
                    string_format += "\n"
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
        try:
            with open(self.subject_data_base, "a") as subject_data:
                for sub in subjects:
                    string_format = sub.__str__() + "\n"
                    subject_data.write(string_format)
        except FileNotFoundError:
            raise FileNotFoundError()

    def retrive_student(self, ind_number):
        try:
            with open(self.student_data_base, "r") as student_data:
                lines = student_data.readlines()
        except FileNotFoundError:
            raise FileNotFoundError()

        for line in lines:
            l = line.split(";")
            for i in l:
                print(i)
                print()

        print(str(ind_number) + " not found.")                       

    def __str__(self):
        return "Course: {} Main Professor: {}".format(self.course_title, self.course_professor.full_name)

# Driver code
if __name__ == "__main__":
    # kreira profesora i smer
    prof = Professor("Nikola","Jorgovanovic","redovni profesor")
    biomedical_engineering = Course("Biomedical engineering", 60, prof)

    # Dodaj predmete sa profesorima u bazu
    Spasic = Professor("Dragan","Spasic", "redovni profesor")
    Okuka = Professor("Aleksandar","Okuka", "asistent")

    mehanika = ProfessorSubject("Mehanika", "101", 9)
    mehanika.add_professors(Spasic, Okuka)
    a = Assignment("Statika", datetime(2021, 1, 30))
    mehanika.add_assignements(a)

    Segedinac = Professor("Milan","Segedinac", "redovni profesor")

    racunarstvo = ProfessorSubject("Racunarstvo", "102", 12)
    racunarstvo.add_professors(Segedinac)

    biomedical_engineering.create_subject_database()
    biomedical_engineering.add_subjects(mehanika, racunarstvo)


    # kreira studente
    Sale = Student("Aleksandar","Fa","aleksandarfa@devgmail.com", 1, "Biomedical engineering","budget")
    Marko = Student("Marko","Maric", "markomaric@gmail.com", 1, "Biomedical engineering", "personal")

    # kreiraj predmet
    oet = Subject("Elektrotehnika", "101",8)
    oet.add_assignements(Assignment("Elektrostatika",datetime(2019,1,10)))
    oet.add_assignements(Assignment("Elektrodinamika",datetime(2019,1,12)))
    print("#"*40)
    Sale.add_subjects(oet)
    Sale.change_assignement_points("Elektrotehnika","Elektrostatika", 40)
    Sale.change_assignement_points("Elektrotehnika","Elektrodinamika", 40)
    Sale.forward_subject("Elektrotehnika")
    Sale.print_subjects(passed=True)
    print("#"*40)
    # upisi studente
    biomedical_engineering.enroll_student(Sale)
    #biomedical_engineering.enroll_student(Marko)

    biomedical_engineering.retrive_student("BE1-2020")

    #aleksandar = biomedical_engineering.retrive_student("BE1-2020")
    #print(aleksandar)

    
