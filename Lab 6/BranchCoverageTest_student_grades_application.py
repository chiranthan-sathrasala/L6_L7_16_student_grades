import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

#Example test cases:
def test_s_grade():
    assert letter_grade(95) == "S"

def test_eligible():
    assert exam_eligibility(80, True, False) == "eligible"

#Write the rest of the test cases so that the code is 90- 100% covered.
# ---- letter_grade ----
def test_invalid_marks_negative():
    with pytest.raises(ValueError):
        letter_grade(-1)

def test_a_grade():
    assert letter_grade(85) == "A"

def test_b_grade():
    assert letter_grade(75) == "B"

def test_c_grade():
    assert letter_grade(65) == "C"

def test_d_grade():
    assert letter_grade(55) == "D"

def test_e_grade():
    assert letter_grade(45) == "E"

def test_f_grade():
    assert letter_grade(30) == "F"

# ---- final_marks ----
def test_final_marks_out_of_range():
    with pytest.raises(ValueError):
        final_marks(41, 50, False)

def test_final_marks_no_project():
    assert final_marks(30, 40, False) == 70

def test_final_marks_with_project():
    assert final_marks(30, 40, True) == 75

def test_final_marks_capped_at_100():
    assert final_marks(40, 60, True) == 100

# ---- exam_eligibility ----
def test_fees_not_paid():
    assert exam_eligibility(90, False, False) == "blocked"

def test_eligible_with_medical():
    assert exam_eligibility(70, True, True) == "eligible"

def test_detained():
    assert exam_eligibility(50, True, False) == "detained"
# ---- Edge cases: letter_grade boundaries ----
def test_marks_zero_is_valid():
    assert letter_grade(0) == "F"

def test_marks_hundred_is_valid():
    assert letter_grade(100) == "S"

def test_marks_above_hundred_invalid():
    with pytest.raises(ValueError):
        letter_grade(101)

def test_grade_boundaries():
    assert letter_grade(90) == "S"
    assert letter_grade(89) == "A"
    assert letter_grade(80) == "A"
    assert letter_grade(79) == "B"
    assert letter_grade(70) == "B"
    assert letter_grade(69) == "C"
    assert letter_grade(60) == "C"
    assert letter_grade(59) == "D"
    assert letter_grade(50) == "D"
    assert letter_grade(49) == "E"
    assert letter_grade(40) == "E"
    assert letter_grade(39) == "F"

# ---- Edge cases: final_marks ----
def test_final_marks_external_out_of_range():
    with pytest.raises(ValueError):
        final_marks(20, 61, False)

def test_final_marks_max_without_project():
    assert final_marks(40, 60, False) == 100

def test_final_marks_project_exactly_100():
    assert final_marks(40, 55, True) == 100

# ---- Edge cases: exam_eligibility ----
def test_attendance_exactly_75():
    assert exam_eligibility(75, True, False) == "eligible"

def test_attendance_74_no_medical():
    assert exam_eligibility(74, True, False) == "detained"

def test_attendance_exactly_65_with_medical():
    assert exam_eligibility(65, True, True) == "eligible"

def test_attendance_64_with_medical():
    assert exam_eligibility(64, True, True) == "detained"

def test_attendance_65_without_medical():
    assert exam_eligibility(65, True, False) == "detained"