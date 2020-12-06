from datetime import datetime
import course
import os

class StudentService:
    def __init__(self, institution, inst_name):
        self.institution = institution
        self.inst_name = inst_name
        self.directory = "Data_Base"
        self.parent_dir = os.getcwd()
        self.path = os.path.join(self.parent_dir, self.directory)

        # Create a data base directory where all info will be stored
        try:
            os.mkdir(self.path)
            print("Directory {} successfuly created.".format(self.directory))
        except OSError as err:
            print(err)

    def create_course(self, course_name, student_num, course_professor):
        """ Creates course for given institution """
        print(self.path)
        c = course.Course(course_name, student_num, course_professor, self.path)
        return c

    def creat_logs(self):
        """ Creates log files
            Should be used only once, or all logs will be deleted.
         """
        with open(self.path+"/logs.txt", "w") as logs:
            logs.write("*"*50 + "LOGS" + "*"*50 + "\n\n")

    def create_user(self, user_name, password, access_type):
        """ Creates user """
        if access_type.lower() not in ("student", "professor", "admin"):
            print("Wrong access type.")
            return None
        
        # Check if there is user with same access type and user name
        # If there are no users in logs that alredy have that access type and user name
        # add that user
        with open(self.path+"/logs.txt", "r+") as logs:
            lines = logs.readlines()
            for line in lines[2:]:
                u_name = line.split(";")[0]
                a_type = line.split(";")[2]
                name = u_name.split(":")[1]
                access = a_type.split(":")[1].strip("\n")
                if (access == access_type):
                    if name == user_name:
                        print("User with access type: {} and user_name: {} alredy exists.".format(access_type, user_name))
                        return None
            string_format = "username:{};password:{};access:{}\n".format(user_name, password, access_type)
            logs.write(string_format)       

    def login(self, user_name, password, access_type):
        found_logs = []
        with open (self.path+"/logs.txt", "r") as logs:
            lines = logs.readlines()

            # Since users of different access can have the same name
            # It is necessery to collect only users with passed access_type
            for line in lines[2:]:
                temp_access = line.split(";")[2]
                access = temp_access.split(":").strip("\n")
                if access == access_type:
                    # User name
                    u_name = line.split(";")[0]
                    name = u_name.split(":")[1]

                    # Password
                    p_word = line.split(";")[1]
                    word = p_word.split(":")[1]
                    found_logs.append({"user_name":name, "password":word})


        for user in found_logs:
            if user["user_name"] == user_name and user["password"] == password:
                return True

        return False

        
        
if __name__ == "__main__":
    ftn = StudentService("University", "Fakultet tehnickih nauka")
    c = ftn.create_course("Biomedical engineering", 60, course.Professor("Nikola","Jorgovanovic","redovni profesor"))
    c.create_subject_database()
    sub1 = course.ProfessorSubject("Mehanika","101",10)
    sub1.add_professors(course.Professor("Dragan", "Spasic","redovni profesor"))
    sub2 = course.ProfessorSubject("Elektronika", "102", 12)
    sub2.add_professors(course.Professor("Goran","Stojanovic", "redovni profesor"))
    c.add_subjects(sub1, sub2)

    c.enroll_student(course.Student("Aleksandar","Fa","aleksandarfadev@gmail.com", 1, "Biomedical engineering","budget"))
    sale = c.pull_student("BE1-2020")
    print(sale)
    sub1 = course.Subject("Mehanika", "101",10)
    sub2 = course.Subject("Elektronika", "101",10)
    sub1.add_assignements(course.Assignment("Statika", datetime(2019, 1, 10)), course.Assignment("Dinamika", datetime(2019,2,10)))
    sale.add_subjects(sub1, sub2)
    sale.change_assignement_points("Mehanika","Statika", 50)
    sale.change_assignement_points("Mehanika","Dinamika", 50)
    sale.forward_subject("Mehanika")
    sale.print_subjects(passed = True)
    c.push_students(sale)
    print("*"*60)
    sale.print_subjects()
    print(sale)

    ftn.creat_logs()
    ftn.create_user("Aca", "asd1231f#$%", "admin")
    ftn.create_user("Aca2", "asd1231f#$%", "admin")



        