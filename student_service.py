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
        c = course.Course(course_name, student_num, course_professor, path=self.path)
        print(c)

        