from datetime import datetime
from subject import Assignment, Subject
from student import Student
import json

class Assign2Dict(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Assignment):
            return {
                "title":obj.title,
                "due_date":obj.due_date.strftime("%b %d %Y")
            }
        return super().default(obj)

class Sub2Dict(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Subject):
            return {
                "title":obj.title,
                "code":obj.code,
                "ESPB":obj.ESPB,
                "grade":obj.grade,
                "forwared":obj.forwared,
                #"assignements":{str(ind):json.dumps(assign, cls = Assign2Dict) for ind, assign in enumerate(obj.assignements)}
                "assignements":[json.dumps(assign, cls = Assign2Dict) for ind, assign in enumerate(obj.assignements)],
                "passed":obj.passed
            }
        return super().default(obj)


class Student2Dict(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Student):
            return {
                "first_name":obj.first_name,
                "last_name":obj.last_name,
                "email":obj.email,
                "year":obj.year,
                "course":obj.course,
                "funding":obj.funding,
                "ESPB":obj.ESPB,
                "index_number":obj.index_number,
                 "subjects":[json.dumps(sub, cls = Sub2Dict) for ind, sub in enumerate(obj.subjects)],
                 "passed_subs":[json.dumps(sub, cls = Sub2Dict) for ind, sub in enumerate(obj.passed_subs)],
                 "average_grade":obj.average_grade
               # "subjects":{str(ind):json.dumps(sub, cls = Sub2Dict) for ind, sub in enumerate(obj.subjects)},
               # "passed_subs":{str(ind):json.dumps(sub, cls = Sub2Dict) for ind, sub in enumerate(obj.passed_subs)}
            }
        return super().default(obj)

        