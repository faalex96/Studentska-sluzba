from person import Person
from subject import Subject
from new_exceptions import WrongType
""" Different design, all searches for subjects will be done by subject code, not by subject title! """

class ProfessorSubject(Subject):
    def __init__(self, title, code, ESPB):
        super().__init__(title, code, ESPB)
        self.professors = []
    
    def add_professors(self, *teachers):
        """ Adds professors to professorsSubject """
        # All or none
        for pr in teachers:
            if not isinstance(pr, Professor):
                raise WrongType(type(pr), Professor)
        
        for pr in teachers:
            self.professors.append(pr)
                

    def __str__(self):
        return "#{0} \"{1:<30s}\", ESPB:{2:2s}, Teaches: {3:<20s}".format(self.code, self.title, str(self.ESPB), self.professors[0].full_name)

class Professor(Person):
    def __init__(self, first_name, last_name, title):
        super().__init__(first_name, last_name)
        self.title = title
        self.email = None
        self.cabinet = None

    def remove_subjects(self, *codes):
        """Removes subjects defined by subject code. This means this teacher can no longer teach that specific subject."""
        for c in codes:
            for sub in self.subjects:
                if sub.code == c:
                    self.subjects.remove(sub)

        #print("Professor {} doesn't teach {}.".format(self.full_name, code))

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

# Driver code
if __name__ == "__main__":
    # Kreiraj profesora
    p = Professor("Goran","Stojanovic", "redovni profesor")
    p2 = Professor("Natasa","Nesto","asistent")
    p.set_info(email="goranstojanovic@uns.ac.rs", cabinet="A202")
    print(p)
    # Kreiraj predmet
    elektronika = ProfessorSubject("Elektronika", "101", 5)
    medicinska_elektronika = ProfessorSubject("Medicinska Elektronika", "102", 5)
    materijali = ProfessorSubject("Matrijali Fabrikacije", "103", 5)
    p.add_subjects(elektronika, medicinska_elektronika, materijali)
    elektronika.add_professors(p, p2, [])


