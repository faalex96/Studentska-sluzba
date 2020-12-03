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

