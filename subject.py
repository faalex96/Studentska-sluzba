from datetime import datetime
import new_exceptions as excp

class Assignment:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.points = 0

    def change_points(self, point):
        """Can't change points before due date for assignment"""
        if datetime.now() > self.due_date:
            self.points = point
        else:
            print("Due date for this assignment has not passed. Can't change points.")

    def __str__(self):
        return "\"{0:<20s}\", {1}, points:{2}".format(self.title, self.due_date.strftime("%b %d %Y"), self.points)


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
        # All or none
        for a in assign:
            if not isinstance(a, Assignment):
                raise excp.WrongType(type(a), Assignment)
                
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
        self.pas = False
        if self.calculate_grade() >= 50:
            self.pas = True
            return self.pas
        return self.pas

    @passed.setter
    def passed(self, value):
        """ Setter for passed property """
        self.pas = value

    def forward_sub(self):
        """ Change forward subject to True. """
        self.forwared = True

    def find_assignement(self, assign_title):
        """Return assignement under specified title"""
        for assign in self.assignements:
            if assign.title == assign_title:
                return assign
        raise excp.AssignmentError(assign_title)

    def print_assignements(self):
        """Prints all assignements"""
        for assign in self.assignements:
            print(assign)
    
    def __str__(self):
        return "#{0} \"{1:^20s}\", ESPB:{2:2s}, GRADE:{3}".format(self.code, self.title, str(self.ESPB), self.grade)
    


if __name__ == "__main__":
    pass
    