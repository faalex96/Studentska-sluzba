from person import Person
from professor import Professor, ProfessorSubject
from student import Student
from subject import Assignment, Subject
from datetime import datetime
from costum_json import Student2Dict
import os
import json


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


    def push_student(self, student):
        """Checks if the course capacity is not full. Generates students index_number. Add student to his datebase."""
        if self.__student_index <= self.students_num:
            if student.course == self.course_title:
                student.index_number =  "{}{}-{}".format(self.course_acronym, self.__student_index, str(self.__course_generation))    
                self.__student_index += 1
                string_format = json.dumps(student, cls=Student2Dict)
                

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

    def retrive_subjects(self, serilized_subs):
        retrived_subs = []
        subs_of_strings = serilized_subs
        subs_of_dicts = [json.loads(sub) for sub in subs_of_strings]

        # Iterate over all subjects
        for sub in subs_of_dicts:
            # Get current_assignements - list full of dicts
            current_assigns = [json.loads(assign) for assign in sub["assignements"]]

            # Create subject object
            retrived_subject = Subject(sub["title"], sub["code"], sub["ESPB"])
            retrived_subject.grade = sub["grade"]
            retrived_subject.forwared = sub["forwared"]
            retrived_subject.passed = sub["passed"]
            

            # Create assignements objects and add them to retrived subject
            for assign in current_assigns:
                retrived_date_str = assign["due_date"]
                retrived_date = datetime.strptime(retrived_date_str, "%b %d %Y")
                retrived_assign = Assignment(assign["title"],retrived_date)
                retrived_subject.add_assignements(retrived_assign)
            
            retrived_subs.append(retrived_subject)
                
        return retrived_subs

    def pull_student(self, ind_number):
        """ Retrives student from student_database """
        try:
            with open(self.student_data_base, "r+") as student_data:
                lines = student_data.readlines()
                for line in lines[2:]:
                    d = json.loads(line)

                    if ind_number == d["index_number"]:
                        retrived_student = Student(d["first_name"],d["last_name"],d["email"],d["year"],d["course"],d["funding"])
                        retrived_student.ESPB = d["ESPB"]
                        retrived_student.index_number = d["index_number"]
                        retrived_student.average_grade = d["average_grade"]
                        
                        subs_of_strings = d["subjects"]
                        pass_of_strings = d["passed_subs"]

                        retrived_subs = self.retrive_subjects(subs_of_strings)
                        retrived_passed = self.retrive_subjects(pass_of_strings)
                        retrived_student.add_subjects(*retrived_subs)

                        for el in retrived_passed:
                            retrived_student.passed_subs.append(el)
                
                        return retrived_student

                print(str(ind_number) + " not found.")  

        except FileNotFoundError:
            raise FileNotFoundError()
                     

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

    # kreiraj predmet i dodaj mu zadatke
    oet = Subject("Elektrotehnika", "101",8)
    oet.add_assignements(Assignment("Elektrostatika",datetime(2019,1,10)))
    oet.add_assignements(Assignment("Elektrodinamika",datetime(2019,1,12)))

    # kreiraj predmet i dodaj mu zadatke
    rac = Subject("Racunarstvo", "102",10)
    rac.add_assignements(Assignment("Petlje",datetime(2019,1,10)))
    rac.add_assignements(Assignment("OOP",datetime(2019,1,10)))

    print("#"*40)
    # Dodaj predmete studentu
    Sale.add_subjects(oet, rac)

    # Promeni poene i prosledi
    Sale.change_assignement_points("Elektrotehnika","Elektrostatika", 40)
    Sale.change_assignement_points("Elektrotehnika","Elektrodinamika", 40)
    Sale.forward_subject("Elektrotehnika")
    
    # upisi studente
    biomedical_engineering.push_student(Sale)
    biomedical_engineering.push_student(Marko)

    #student = biomedical_engineering.retrive_student("BE1-2020")
    #student.print_subjects(passed = True)

    marko = biomedical_engineering.pull_student("BE2-2020")
    marko.add_subjects(oet, rac)
    
    marko.change_assignement_points("Racunarstvo", "Petlje", 40)
    marko.change_assignement_points("Racunarstvo", "OOP", 60)
    marko.forward_subject("Racunarstvo")
    marko.print_subjects(passed=True)
    biomedical_engineering.push_student(marko)
    m = biomedical_engineering.pull_student("BE2-2020")
    print(m)
    
    

    
    

    
