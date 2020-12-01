from datetime import datetime

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        """Returns full name of a person."""
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
        self.forwared = False

    def add_assignements(self, *assign):
        """Adds assignement into subject assignements list"""
        for a in assign:
            self.assignements.append(a)

    def calculate_grade(self):
        """Calculates grade based on assignment points"""
        total_score = 0
        for assign in self.assignements:
            total_score += assign.points

        if total_score >= 50 and total_score < 60:
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
    
    @property
    def passed(self):
        if self.calculate_grade() >= 50:
            return True
        return False

    def forward_subject(self):
        """ Change forward subject to True. """
        self.forwared = True

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
mehanika.add_assignements(a,a2,a3)
mehanika.print_assignements()

racunarstvo = Subject("Racunarstvo", "101", 12)
racunarstvo.add_assignements(Assignment("OOP", datetime(2020,12,2)))
racunarstvo.add_assignements(Assignment("Concurrency", datetime(2020, 12,10)))


class Student(Person):
    def __init__(self, first_name, last_name, email, year, course, funding):
        super().__init__(first_name, last_name)
        self.email = email
        self.year = year
        self.course = course
        self.funding = funding
        self.subjects = []
        self.passed_subs = []               # Necessary for eliminating multiple forwarding of the same subject
        self.ESPB = 0
    
    def add_subject(self, *subs):
        """ Adds subject to students subjects list"""
        for sub in subs:
            self.subjects.append(sub)

    def find_subject(self, subject_title):
        """ Returns subject under specified title"""
        for sub in self.subjects:
            if sub.title == subject_title:
                return sub

    def print_all_subjects(self):
        """Prints all subjects"""
        for sub in self.subjects:
            print(sub)

    def change_assignement_points(self, subject_title, assignement_title, points):
        """Find subject, and its's assignment and change it's points"""
        subject = self.find_subject(subject_title)
        assign = subject.find_assignement(assignement_title)
        assign.change_points(points)
        subject.calculate_grade()
    
    def forward_subject(self, subject_title):
        """ If subject is passed and forwarded it will show up in passed subject print
        with it's code, title, ESPB point and grade."""
        subject = self.find_subject(subject_title)
        subject.forward_subject()
        if subject.passed and subject.forwared:
            if subject not in self.passed_subs:             # Make sure you don't forward same subject twice
                self.ESPB += subject.ESPB
                self.passed_subs.append(subject)

    def print_passed_subjects(self):
        """ Prints all passed and forwarded subjects"""
        for sub in self.subjects:
            if sub.passed and sub.forwared:
                print(sub)
        #for sub in self.passed_subs:
        #    print(sub)

    def enroll_new_year(self, tresh_year, tresh_budget):
        """There are two ESPB tresholds: year and budget treshold. 
        If student passed year treshold, he can be enrolled to next year.
        If student passed budget treshold, he can be enrolled to next year on budget."""
        if self.ESPB >= tresh_year:
            self.year += 1
            if self.ESPB >= tresh_budget:
                self.funding = "budget"
            else:
                self.funding = "personal"
        else:
            print("Can't enroll student. Not enough ESPB points.")

    @property
    def average_grade(self):
        avg = 0
        for sub in self.passed_subs:
            avg += sub.grade
        return avg/len(self.passed_subs)

    def __str__(self):
        return "{0}, year: {1}. course: {2}, ESPB:{3}, Avg:{4:.2f}, funding: {5}.".format(self.full_name, self.year, self.course, self.ESPB, self.average_grade,self.funding)
        
Sale = Student("Aleksandar","Fa","aleksandarfa@dev.gmail", 1, "Biomedical engineering","budget")
Sale.add_subject(mehanika)
Sale.add_subject(racunarstvo)

Sale.change_assignement_points("Mehanika", "Upravljanje toka programa", 30)
Sale.change_assignement_points("Mehanika", "For i While petlja", 30)
Sale.change_assignement_points("Mehanika", "Funkcije", 30)
Sale.forward_subject("Mehanika")

#Sale.print_all_subjects()
Sale.change_assignement_points("Racunarstvo", "OOP", 30)
Sale.change_assignement_points("Racunarstvo","Concurrency", 21)
Sale.forward_subject("Racunarstvo")
Sale.forward_subject("Racunarstvo")
Sale.print_passed_subjects()
print(Sale)
Sale.enroll_new_year(36, 48)