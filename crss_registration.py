# CRSS main branch - course registration system
class CourseRegistration:

    def __init__(self):
        self.registrations = {}
        self.completed_courses = {}

    def set_completed_courses(self, student_id, courses):
        self.completed_courses[student_id] = courses

    def get_registered_courses(self, student_id):
        return self.registrations.get(student_id, [])

    def validate_student_id(self, student_id):
        if not student_id:
            raise ValueError("Invalid student ID")

    def check_prerequisites(self, student_id, section):
        for prerequisite in section["prerequisites"]:
            if prerequisite not in self.completed_courses.get(student_id, []):
                raise ValueError("Prerequisites not completed")

    def check_timetable_conflict(self, student_id, section):
        for course in self.registrations.get(student_id, []):
            if course["time"] == section["time"]:
                raise ValueError("Timetable conflict")

    def check_seats(self, section):
        if section["seats_available"] <= 0:
            raise ValueError("No seats available")

    def register(self, student_id, section):
        self.validate_student_id(student_id)

        self.check_prerequisites(student_id, section)
        self.check_timetable_conflict(student_id, section)
        self.check_seats(section)

        if student_id not in self.registrations:
            self.registrations[student_id] = []

        self.registrations[student_id].append(section)
        section["seats_available"] -= 1

        return "Registration successful"