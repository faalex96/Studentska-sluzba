class SubjectError(Exception):
    def __init__(self, subject_title):
        self.subject_title = subject_title

    def __str__(self):
        return "Subject \"{}\" not found.".format(self.subject_title)

class AssignmentError(Exception):
    def __init__(self, assign_title):
        self.assign_title = assign_title
    
    def __str__(self):
        return "Assignment \"{}\" not found".format(self.assign_title)

class WrongType(TypeError):
    def __init__(self, type_found, type_needed):
        self.type_found = str(type_found)[8:-2]    # Isolate just type from string '<class "typeX">'
        self.type_needed = type_needed.__name__

    def __str__(self):   
        return "{} object is required (got type {})".format(self.type_needed, self.type_found)
