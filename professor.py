from student import Person
from student import Subject
""" Different design, all searches for subjects will be don by subject code, not by subject title! """

class ProfessorSubject(Subject):
    def __init__(self, title, code, ESPB, professor):
        super().__init__(title, code, ESPB)
        self.professor = professor

    def __str__(self):
        return "#{0} \"{1:<30s}\", ESPB:{2:2s}, Teaches: {3:<20s}".format(self.code, self.title, str(self.ESPB), self.professor.full_name)

class Professor(Person):
    def __init__(self, first_name, last_name, title):
        super().__init__(first_name, last_name)
        self.title = title
        self.teaches = []
        self.email = None
        self.cabinet = None

    def add_subjects(self, *subs):
        """ Add subject that professor teaches """
        for sub in subs:
            self.teaches.append(sub)

    def remove_subjects(self, *codes):
        """Removes subjects defined by subject code. This means this teacher can no longer teach that specific subject."""
        for c in codes:
            for sub in self.teaches:
                if sub.code == c:
                    self.teaches.remove(sub)

        #print("Professor {} doesn't teach {}.".format(self.full_name, code))

    def print_subjects(self):
        """ Prints subject that professor teaches"""
        for sub in self.teaches:
            print(sub)

    def set_info(self, email, cabinet):
        """ Set professor information """
        self.email = email
        self.cabinet = cabinet

    def change_title(self, new_title):
        """ Change professors title"""
        self.title = new_title

    def __str__(self):
        if None in (self.email, self.cabinet):
            return "{0:^20s} {1:<30s}".format(self.title, self.full_name)
        else:
            return "{0:<20s} {1:<20s} email: {2:<20s} cabinet: {3:<20s}".format(self.title, self.full_name, self.email, self.cabinet)

# Kreiraj profesora
p = Professor("Goran","Stojanovic", "redovni profesor")
p.set_info(email="goranstojanovic@uns.ac.rs", cabinet="A202")
print(p)
# Kreiraj predmet
elektronika = ProfessorSubject("Elektronika", "101", 5, p)
medicinska_elektronika = ProfessorSubject("Medicinska Elektronika", "102", 5, p)
materijali = ProfessorSubject("Matrijali Fabrikacije", "103", 5, p)
p.add_subjects(elektronika, medicinska_elektronika, materijali)
p.print_subjects()
print("#"*50)
p.remove_subjects("103", "102")
p.print_subjects()

