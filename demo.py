import datetime as dt
import student_service as ss
import course 

# This is demo of my package

# Create student service
s_service = ss.StudentService("College", "Faculty of Technical Sciences")

# Create logs and admin
s_service.creat_logs()
s_service.create_user("FirstAdmin", "not1234", "admin")

# Lets create a course
created_course = s_service.create_course("Biomedical Engineering", 60, course.Professor("Nikola", "Jorgovanovic", "professor"))

# Create course subject
computer_science = course.ProfessorSubject("Computer Science", "101", 10)
# Create professor
professor = course.Professor("Milan", "Segedinac", "professor")
# Add professor to created subject
computer_science.add_professor(professor)
# Add created subject to course data base
created_course.push_subjects(computer_science)

# Create course subject
algebra = course.ProfessorSubject("Algebra", "102", 10)
# Create professor
professor2 = course.Professor("Sandra", "Buhmiler", "professor")
# Add professor to created subject
algebra.add_professor(professor2)
# Add created subject to course data base
created_course.push_subjects(algebra)

# Create a student
student = course.Student("Aleksandar", "Fa", "aleksandarfadev@gmail.com", 1, "Biomedical Engineering", "state budget")

# Create student subjects
sub1 = course.Subject("Computer Science","101", 10)
sub2 = course.Subject("Algebra", "102", 10)

# Create assignements for subjects
sub1_a1 = course.Assignment("Loops",dt.datetime(2019, 10, 1))
sub1_a2 = course.Assignment("OOP", dt.datetime(2019, 11, 1))

sub2_a1 = course.Assignment("Functions",dt.datetime(2019, 10, 1))
sub2_a2 = course.Assignment("Vectors", dt.datetime(2019, 11, 1))

# Add assignements tu student subject
sub1.add_assignements(sub1_a1,sub1_a2)
sub2.add_assignements(sub2_a1, sub2_a2)

# Add subjects to student
student.add_subjects(sub1, sub2)

# Enroll student to a course
created_course.enroll_student(student)

# Lets retrive student from course
Aleksandar = created_course.pull_student("BE1-2020")
print(Aleksandar)

# Lets change Aleksandars assignement points
Aleksandar.change_assignement_points("Computer Science", "Loops", 50)
Aleksandar.change_assignement_points("Computer Science", "OOP", 50)

# Lets forward Aleksandar subject Computer science
Aleksandar.forward_subject("Computer Science")

# And lets return modified Aleksandar to data base
created_course.push_students(Aleksandar)

# Lets pull him again just to see which subjects has he passed
Aleksandar = created_course.pull_student("BE1-2020")
print("Aleksandars passed subjects")
Aleksandar.print_subjects(passed = True)

# Lets change assignements points to algebra but not forward the subject
Aleksandar.change_assignement_points("Algebra","Functions", 50)
Aleksandar.change_assignement_points("Algebra","Vectors", 49)
print("Aleksandars passed subject after changing algebra points but not forwarding algebra")
Aleksandar.print_subjects(passed = True)

# Return modified Aleksandar to data base

created_course.push_students(Aleksandar)










