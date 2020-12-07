from person import Person
from subject import Subject
from new_exceptions import WrongType
""" Different design, all searches for subjects will be done by subject code, not by subject title! """

class ProfessorSubject(Subject):
    def __init__(self, title, code, ESPB):
        super().__init__(title, code, ESPB)
        self.professor = None
    
    def add_professor(self, pr):
        """ Adds professor to professorsSubject """
        if not isinstance(pr, Professor):
            raise WrongType(type(pr), Professor)
        
        self.professor = pr

    def remove_professor(self, name, last_name):
        """ Removes professor defined by their full name """
        if self.professor.full_name == "{} {}".format(name, last_name):
            self.professor = ""
        else:
            print("{} {} not found".format(name, last_name))

    def __str__(self):
        try:
            return "#{0}, \"{1:<30s}\", ESPB:{2:2s}, Teaches: {3:<20s}".format(self.code, self.title, str(self.ESPB), self.professor.full_name)
        except AttributeError:
            return "This subject needs professor."

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
    pass


