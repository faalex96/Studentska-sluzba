from person import Person
from professor import Professor, ProfessorSubject
from student import Student
from subject import Assignment, Subject
from datetime import datetime
from costum_json import Student2Dict
from new_exceptions import WrongType
import json
import os

class Course:
    def __init__(self, course_title, students_num, course_professor, path=None):

        """ Initilize the title of the course and professor that represents it"""
        self.course_title = course_title
        self.course_professor = course_professor
        self.__course_generation = datetime.now().year
        self.path = path

        # If course was created with path argument not being None
        # Than there would be created a folder for course 
        # All the files would be in that folder
        if self.path == None:
            path_string = os.getcwd()
        else:
            path_string = self.path + "/{}".format(self.course_title)
            try:
                os.mkdir(path_string)
            except OSError as err:
                print(err)

        self.student_data_base = path_string+"/{}_{}_data.txt".format(self.course_title, self.__course_generation)
        self.subject_data_base = path_string+"/{}_subjects_data.txt".format(self.course_title)
        self.__student_index = 1
        self.students_num = students_num

        # Create datebase when course is created
        try:
            with open(self.student_data_base, "w") as data_base:
                string_format = "*"*50 + " {} {}".format(self.course_title, self.__course_generation) + "*"*50 + "\n\n"     
                data_base.write(string_format)
        except FileNotFoundError:
            raise FileNotFoundError()

    def push_students(self, *students):
        """ Adds students to data base """
        # Test if passed "students" are required type 
        # All or none, if some obj in students is not  Student instance
        # no student is writen to file
        for student in students:
            if not isinstance(student, Student):
                raise WrongType(type(student), Student)
            
        try:
            with open(self.student_data_base, "a") as data_base:
                for student in students:
                    string_format = json.dumps(student, cls=Student2Dict)     # serialize student 
                    string_format += "\n"
                    data_base.write(string_format)
        except FileNotFoundError:
                raise FileNotFoundError()
            
        
    
    def enroll_student(self, student):
        """Checks if the course capacity is not full. Generates students index_number. Add student to his datebase."""
        if not isinstance(student, Student):
            raise WrongType(type(student), Student)

        if self.__student_index <= self.students_num:
            if student.course == self.course_title:
                student.index_number = "{}{}-{}".format(self.course_acronym, self.__student_index, str(self.__course_generation))
                self.__student_index += 1
                self.push_students(student) # Adds to data base
            else:
                print("Wrong course.")
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
        try:
            with open(self.subject_data_base, "w") as subjects_data:
                subjects_data.write("*"*50 + self.course_title + "*"*50 + "\n\n")
        except FileNotFoundError:
            raise FileNotFoundError()

    def push_subjects(self, *subjects):
        """ Adds ProfessorSubject to subjects of course """
        # All or none
        for sub in subjects:
            if not isinstance(sub, ProfessorSubject):
                raise WrongType(type(sub), ProfessorSubject)

        try:
            with open(self.subject_data_base, "a") as subject_data:
                for sub in subjects:
                    string_format = sub.__str__() + "\n"
                    subject_data.write(string_format)
        except FileNotFoundError:
            raise FileNotFoundError()
    
    @staticmethod
    def retrive_subjects(serilized_subs):
        """ Retrives subjects from string """
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
                retrived_assign.points = assign["points"]
                retrived_subject.add_assignements(retrived_assign)
            
            retrived_subs.append(retrived_subject)
                
        return retrived_subs

    def pull_student(self, ind_number):
        """ Retrives student from student_database """
        retrived_student = None
        try:
            # First open in read mode
            with open(self.student_data_base, "r") as student_data:
                lines = student_data.readlines()

            # Second open in write mode: write first two lines, write lines that don't match ind number
            # Don't write lines that match ind number - this way once student is pulled he won't be in file anymore
            # Push student back to file after modification
            with open(self.student_data_base, "w") as student_data:
                
                for ind, line in enumerate(lines):
                    if ind < 2:
                        student_data.write(line)    # Write first two lines, header of the file
                    elif ind >= 2:
                        d = json.loads(line)
                        if ind_number != d["index_number"]:
                            student_data.write(line)
                        else:
                            retrived_student = Student(d["first_name"],d["last_name"],d["email"],d["year"],d["course"],d["funding"])
                            retrived_student.ESPB = d["ESPB"]
                            retrived_student.index_number = d["index_number"]
                            retrived_student.average_grade = d["average_grade"]
                            
                            subs_of_strings = d["subjects"]
                            pass_of_strings = d["passed_subs"]

                            retrived_subs = Course.retrive_subjects(subs_of_strings)
                            retrived_passed = Course.retrive_subjects(pass_of_strings)
                            retrived_student.add_subjects(*retrived_subs)

                            for el in retrived_passed:
                                retrived_student.passed_subs.append(el)
                
                
                if retrived_student != None:
                    return retrived_student
                else:
                    print(str(ind_number) + " not found.")  

        except FileNotFoundError:
            raise FileNotFoundError()

    def pull_subject(self, code):
        retrived_sub = None
        with open(self.subject_data_base, "r") as data_base:
            lines = data_base.readlines()

        with open(self.subject_data_base, "w") as data_base:
            # Write lines 0 and 1 - header of the file
            data_base.write(lines[0])
            data_base.write(lines[1])
            
            for line in lines[2:]:
                code_found, title, espb, professor = line.split(",")

                if code_found.strip("#") == code:
                    retrived_sub = ProfessorSubject(title.strip(), code_found.strip("#"), int(espb.strip().split(":")[1]))
                    full_name = professor.lstrip().split(":")
                    full_name = full_name[1].strip("\n").strip()
                    first, last = full_name.split(" ")
                    retrived_sub.add_professors(Professor(first, last, ""))
                else:
                    data_base.write(line)

        if retrived_sub != None:
            return retrived_sub
        else:
            print(str(code) + " not found.")
                     

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
    biomedical_engineering.push_subjects(mehanika, racunarstvo)


    # kreira studente
    Sale = Student("Aleksandar","Fa","aleksandarfa@devgmail.com", 1, "Biomedical engineering","budget")
    Marko = Student("Marko","Maric", "markomaric@gmail.com", 1, "Biomedical engineering", "personal")

    # upisi studente
    biomedical_engineering.enroll_student(Sale)
    biomedical_engineering.enroll_student(Marko)

    # kreiraj predmet i dodaj mu zadatke
    oet = Subject("Elektrotehnika", "101",8)
    oet.add_assignements(Assignment("Elektrostatika",datetime(2019,1,10)))
    oet.add_assignements(Assignment("Elektrodinamika",datetime(2019,1,12)))

    # kreiraj predmet i dodaj mu zadatke
    rac = Subject("Racunarstvo", "102",10)
    rac.add_assignements(Assignment("Petlje",datetime(2019,1,10)))
    rac.add_assignements(Assignment("OOP",datetime(2019,1,10)))

   # Vrati saleta i dodaj mu predmete
    sale = biomedical_engineering.pull_student("BE1-2020")
    sale.add_subjects(oet, rac)
    sale.change_assignement_points("Elektrotehnika", "Elektrostatika", 25)
    sale.change_assignement_points("Elektrotehnika", "Elektrodinamika", 26)
    sale.forward_subject("Elektrotehnika")
    print("First")
    sale.find_subject("Elektrotehnika").print_assignements()
    biomedical_engineering.push_students(sale)
    sale = biomedical_engineering.pull_student("BE1-2020")
    sale.change_assignement_points("Racunarstvo", "Petlje", 50)
    sale.change_assignement_points("Racunarstvo", "OOP", 50)
    sale.forward_subject("Racunarstvo")
    print("Second")
    sale.print_subjects(passed = True)
    biomedical_engineering.push_students(sale)
    sale = biomedical_engineering.pull_student("BE1-2020")
    print("Third")
    sale.print_subjects(passed = True)
    print(sale)
    biomedical_engineering.push_students(sale)

    Nina = Student("Nevena","Dragic", "nenva@gmail.com","1", "Biomedical engineering", "budget")
    biomedical_engineering.enroll_student(Nina)
    nina = biomedical_engineering.pull_student("BE3-2020")
    nina.add_subjects(oet, rac)
    nina.change_assignement_points("Elektrotehnika","Elektrodinamika", 50)
    nina.change_assignement_points("Elektrotehnika","Elektrostatika", 50)
    nina.forward_subject("Elektrotehnika")
    biomedical_engineering.push_students(nina)
    nina = biomedical_engineering.pull_student("BE3-2020")
    print(nina)
    nina.print_subjects()
    nina.change_assignement_points("Racunarstvo","Petlje",50)
    nina.change_assignement_points("Racunarstvo","OOP",50)
    nina.forward_subject("Racunarstvo")
    print("*"*59)
    nina.print_subjects(passed=True)
    print(nina)
    biomedical_engineering.push_students(nina)
    #sub = biomedical_engineering.pull_subject("101")

    sub = biomedical_engineering.pull_subject("102")
    print(sub)
    
    

    
    

    
