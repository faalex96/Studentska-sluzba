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
    pass



        