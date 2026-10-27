import pytest
from crss_registration import CourseRegistration


@pytest.fixture
def crss():
    return CourseRegistration()


def sample_section(**overrides):
    section = {
        "code": "CSE101",
        "name": "Introduction to Programming",
        "time": "Mon 10:00-11:00",
        "prerequisites": [],
        "seats_available": 5,
    }
    section.update(overrides)
    return section


def test_student_can_register_for_course(crss):
    result = crss.register("S001", sample_section())
    assert result == "Registration successful"
    assert len(crss.get_registered_courses("S001")) == 1


def test_registration_is_saved_for_student(crss):
    section = sample_section()
    crss.register("S001", section)
    assert crss.get_registered_courses("S001")[0]["code"] == "CSE101"


def test_student_without_prerequisite_is_rejected(crss):
    section = sample_section(prerequisites=["CSE100"])
    with pytest.raises(ValueError, match="Prerequisites not completed"):
        crss.register("S001", section)


def test_student_with_prerequisite_can_register(crss):
    crss.set_completed_courses("S001", ["CSE100"])
    section = sample_section(prerequisites=["CSE100"])
    assert crss.register("S001", section) == "Registration successful"


def test_timetable_conflict_is_rejected(crss):
    crss.register("S001", sample_section())
    another = sample_section(code="CSE102", time="Mon 10:00-11:00")
    with pytest.raises(ValueError, match="Timetable conflict"):
        crss.register("S001", another)


def test_registration_rejected_when_no_seats(crss):
    section = sample_section(seats_available=0)
    with pytest.raises(ValueError, match="No seats available"):
        crss.register("S001", section)


def test_seat_count_decreases_after_registration(crss):
    section = sample_section(seats_available=3)
    crss.register("S001", section)
    assert section["seats_available"] == 2


def test_students_have_separate_registration_lists(crss):
    crss.register("S001", sample_section())
    crss.register("S002", sample_section(code="CSE102", time="Tue 10:00-11:00"))
    assert len(crss.get_registered_courses("S001")) == 1
    assert crss.get_registered_courses("S001")[0]["code"] == "CSE101"
    assert crss.get_registered_courses("S002")[0]["code"] == "CSE102"

def test_registration_rejects_invalid_student_id(crss):
    with pytest.raises(ValueError, match="Invalid student ID"):
        crss.register("", sample_section())