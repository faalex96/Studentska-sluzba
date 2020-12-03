from datetime import datetime
from person import Person
from subject import Assignment, Subject

class Student(Person):
    def __init__(self, first_name, last_name, email, year, course, funding):
        super().__init__(first_name, last_name)
        self.email = email
        self.year = year
        self.course = course
        self.funding = funding
        self.passed_subs = []               # Necessary for eliminating multiple forwarding of the same subject
        self.ESPB = 0
        self.index_number = ""

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
    
    def forward_subject(self, subject_title):
        """ If subject is passed and forwarded it will show up in passed subject print
        with it's code, title, ESPB point and grade."""
        subject = self.find_subject(subject_title)
        subject.forward_subject()
        if subject.passed and subject.forwared:
            if subject not in self.passed_subs:             # Make sure you don't forward same subject twice
                self.ESPB += subject.ESPB
                self.passed_subs.append(subject)
                

    def sort_subjects(self, sort_type="grade", sub_type="all"):
        """ Sorts and prints subjects(default = all, passed) by type (default = grade, ESPB) """
        sorting_obj = None          
        if sub_type == "passed":                
            sorting_obj = self.passed_subs
        else:
            sorting_obj = self.subjects             # Even if sub_type is wrong default sorting will be on all subjects

        sorted_subs = sorted(sorting_obj, key = lambda subject: getattr(subject, sort_type), reverse=True)
        self.print_subjects(iterable = sorted_subs)

        return sorted_subs


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
        """ Return students average grade"""
        avg = 0
        if (len(self.passed_subs) > 0):
            for sub in self.passed_subs:
                avg += sub.grade
            return avg/len(self.passed_subs)
        else:
            return 0
            
    def __str__(self):
        return "{0}, year: {1}, course: {2}, ESPB:{3}, Avg:{4:.2f}, funding: {5}.".format(self.full_name, self.year, self.course, self.ESPB, self.average_grade,self.funding)

# Driver code 
if __name__ == "__main__":
    # Zadaci iz mehanike
    a = Assignment("Statika", datetime(2021, 1, 25))
    a2 = Assignment("Dinamika", datetime(2021, 1, 24))
    a3 = Assignment("Kinematika", datetime(2021, 2, 10))

    # Zadaci iz racunarstva
    ra = Assignment("OOP", datetime(2020,12,20))
    ra2 = Assignment("Concurrency", datetime(2020, 12,10))

    # Zadaci iz oet-a
    oa = Assignment("Elektrostatika", datetime(2021, 1, 30))
    oa2 = Assignment("Magnetni Fluks", datetime(2021, 1, 30))
    oa3 = Assignment("Kirhofov Zakon", datetime(2021, 1, 10))

    mehanika = Subject("Mehanika","101",9)
    mehanika.add_assignements(a,a2,a3)

    racunarstvo = Subject("Racunarstvo", "102", 12)
    racunarstvo.add_assignements(ra, ra2)

    oet = Subject("Elektrotehnika", "103", 7)
    oet.add_assignements(oa, oa2, oa3)

    # Napravi studenta i dodaj mu predmete        
    Sale = Student("Aleksandar","Fa","aleksandarfa@dev.gmail", 1, "Biomedical engineering","budget")
    Sale.add_subjects(mehanika, racunarstvo, oet)

    # Promeni poene iz mehanike
    Sale.change_assignement_points("Mehanika", "Statika", 30)
    Sale.change_assignement_points("Mehanika", "Dinamika", 30)
    Sale.change_assignement_points("Mehanika", "Kinematika", 10)
    Sale.forward_subject("Mehanika")

    # Promeni poene iz racunarstva
    Sale.change_assignement_points("Racunarstvo", "OOP", 70)
    Sale.change_assignement_points("Racunarstvo","Concurrency", 30)
    Sale.forward_subject("Racunarstvo")

    # Promeni poene iz oet-a
    Sale.change_assignement_points("Elektrotehnika", "Elektrostatika", 30)
    Sale.change_assignement_points("Elektrotehnika", "Magnetni Fluks", 12)
    Sale.change_assignement_points("Elektrotehnika", "Kirhofov Zakon", 10)
    #Sale.forward_subject("Elektrotehnika")

    # Ispisi
    Sale.sort_subjects()
    


