from new_exceptions import WrongType
from subject import Subject

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.subjects = []

    @property
    def full_name(self):
        """Returns full name of a person."""
        return "{} {}".format(self.first_name, self.last_name)

    @full_name.setter
    def full_name(self, name):
        """ Can be used when retriving person from some file/data_base"""
        first, last = name.split(" ")
        self.first_name = first
        self.last_name = last

    def add_subjects(self, *subs):
        """ Adds subjects to subjects list """
        # All or none
        for subject in subs:
            if not isinstance(subject, Subject):            # ProfessorSubject inherist Subject. Will work for both
                raise WrongType(type(subject), Subject)
        
        for subject in subs:
            self.subjects.append(subject)

    def print_subjects(self, iterable=None, passed=None):
        if iterable == None and passed == None:
            for sub in self.subjects:
                print(sub)
        elif iterable != None and passed == None:
            for sub in iterable:
                print(sub)
        elif iterable == None and passed != None:
            for sub in self.subjects:
                if sub.passed and sub.forwared:
                    print(sub)
        else:
            print("Can't mix iterable and passed arguments together! One or both must be None!")


if __name__ == "__main__":
    p = Person("Pera","Peric")
    #predmet = Subject("mata", "bla",13)
    p.add_subjects([])