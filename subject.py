from datetime import datetime

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


class Subject:
    def __init__(self, title, code, ESPB):
        self.title = title
        self.code = code
        self.ESPB = ESPB
        self.assignements = []
        self.grade = 5
        self.forwared = False
        self.professors = []

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
        return "#{0} \"{1:^20s}\", ESPB:{2:2s}, GRADE:{3}".format(self.code, self.title, str(self.ESPB), self.grade)
    


if __name__ == "__main__":
    mehanika = Subject("Mehanika", "101", 9)
    print(mehanika)