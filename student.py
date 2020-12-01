from datetime import datetime

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class Assignment:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.points = 0

    def change_points(self, point):
        """Can't change points after due date for assignment"""
        if datetime.now() <= self.due_date:
            self.points = point

    def __str__(self):
        return "\"{0:<20s}\", {1}, points:{2}".format(self.title, self.due_date.strftime("%b %d %Y"), self.points)

a = Assignment("Upravljanje toka programa", datetime(2021, 1, 25))
a2 = Assignment("For i While petlja", datetime(2021, 1, 24))
a3 = Assignment("Funkcije", datetime(2021, 2, 10))

class Subject:
    def __init__(self, title, code, ESPB):
        self.title = title
        self.code = code
        self.ESPB = ESPB
        self.assignements = []
        self.grade = 5

    def add_assignement(self, assign):
        """Adds assignement into subject assignements list"""
        self.assignements.append(assign)

    def calculate_grade(self):
        """Calculates grade based on assignment points"""
        total_score = 0
        for assign in self.assignements:
            total_score += assign.points

        if total_score > 50 and total_score < 60:
            self.grade = 6
        elif total_score >= 60 and total_score < 70:
            self.grade = 7
        elif total_score >= 70 and total_score < 80:
            self.grade = 8
        elif total_score >= 80 and total_score < 90:
            self.grade = 9
        elif total_score >= 90:
            self.grade = 10

        return total_score

    def find_assignement(self, assign_title):
        """Return assignement under specified title"""
        for assign in self.assignements:
            if assign.title == assign_title:
                return assign

    def print_assignements(self):
        """Prints all assignements"""
        for assign in self.assignements:
            print(assign)

    def __str__(self):
        return "#{0} \"{1:^20s}\", ESPB:{2:2s} GRADE:{3}".format(self.code, self.title, str(self.ESPB), self.grade)

mehanika = Subject("Mehanika","101",9)
mehanika.add_assignement(a)
mehanika.add_assignement(a2)
mehanika.add_assignement(a3)
mehanika.print_assignements()

class Student(Person):
    def __init__(self, first_name, last_name, email, year, course, funding):
        super().__init__(first_name, last_name)
        self.email = email
        self.year = year
        self.course = course
        self.funding = funding
        self.subjects = []
        self.ESPB = 0
    
    def add_subject(self, subject):
        """ Adds subject to students subjects list"""
        self.subjects.append(subject)

    def find_subject(self, subject_title):
        """ Returns subject under specified title"""
        for sub in self.subjects:
            if sub.title == subject_title:
                return sub

    def change_assignement_points(self, subject_title, assignement_title, points):
        """Find subject, and its's assignment and change it's points"""
        subject = self.find_subject(subject_title)
        assign = subject.find_assignement(assignement_title)
        assign.change_points(points)
        subject.calculate_grade()

    def print_subjects(self):
        """Prints all subjects"""
        for sub in self.subjects:
            print(sub)

    def __str__(self):
        return "{0}, year: {1}, course: {2}, funding: {3}.".format(self.full_name, self.year, self.course, self.funding)
        
Sale = Student("Aleksandar","Fa","aleksandarfa@dev.gmail", 1, "Biomedical engineering","budgete")
Sale.add_subject(mehanika)

Sale.change_assignement_points("Mehanika", "Upravljanje toka programa", 30)
Sale.change_assignement_points("Mehanika", "For i While petlja", 30)
Sale.change_assignement_points("Mehanika", "Funkcije", 30)

Sale.print_subjects()
print()