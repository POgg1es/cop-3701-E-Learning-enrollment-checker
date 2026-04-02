import csv
import random
from datetime import datetime, timedelta

NUM_STUDENTS = 120
NUM_COURSES = 10
NUM_ASSESSMENTS = 50

# -------------------------
# Helper
# -------------------------
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# -------------------------
# STUDENT
# -------------------------
students = []
for i in range(1, NUM_STUDENTS + 1):
    students.append([
        i,
        random.choice(["M", "F"]),
        random.choice(["North", "South", "East", "West"]),
        random.choice(["High School", "Bachelor", "Master"]),
        random.choice(["Low", "Medium", "High"]),
        random.choice(["0-35", "35-55", "55+"]),
        random.choice(["Pass", "Fail", "Distinction"])
    ])

with open("data/students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id_student","gender","region","highest_education","imd_band","age_band","final_result"])
    writer.writerows(students)

# -------------------------
# COURSE
# -------------------------
courses = []
for i in range(1, NUM_COURSES + 1):
    courses.append([
        f"M{i}",
        f"P{i}",
        random.randint(10, 52)
    ])

with open("data/courses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["code_module","code_presentation","module_presentation_length"])
    writer.writerows(courses)

# -------------------------
# ASSESSMENT
# -------------------------
assessments = []
for i in range(1, NUM_ASSESSMENTS + 1):
    course = random.choice(courses)
    assessments.append([
        i,
        course[0],
        course[1],
        random.choice(["Exam","Quiz","Assignment"]),
        random_date(datetime(2022,1,1), datetime(2023,1,1)).date(),
        round(random.uniform(10,100),2)
    ])

with open("data/assessments.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id_assessment","code_module","code_presentation","assessment_type","date","weight"])
    writer.writerows(assessments)

# -------------------------
# STUDENT_REGISTRATION
# -------------------------
registrations = []
for s in students:
    registrations.append([
        s[0],
        random_date(datetime(2022,1,1), datetime(2022,6,1)).date(),
        ""
    ])

with open("data/student_registration.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id_student","date_registration","date_unregistration"])
    writer.writerows(registrations)

# -------------------------
# STUDENT_ASSESSMENT
# -------------------------
student_assessment = []
for s in students:
    for a in random.sample(assessments, 5):
        student_assessment.append([
            s[0],
            a[0],
            random_date(datetime(2022,1,1), datetime(2023,1,1)).date(),
            round(random.uniform(0,100),2)
        ])

with open("data/student_assessment.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id_student","id_assessment","date_submitted","score"])
    writer.writerows(student_assessment)