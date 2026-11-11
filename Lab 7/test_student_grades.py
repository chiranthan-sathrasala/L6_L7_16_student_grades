import re

import pytest
from hypothesis import given, assume, strategies as st
from student_grades import average_marks, parse_srn, short_name

SRN_PATTERN = r"PES[0-9]UG[0-9]{2}[A-Z]{2}[0-9]{3}"
LOWER = "abcdefghijklmnopqrstuvwxyz"


# ---------- 1. No-crash tests (fuzz with random text and None) ----------
# Rejecting bad input with a ValueError is acceptable.
# Any other exception (TypeError, AttributeError, ...) is a bug.

@given(st.text() | st.none())
def test_average_marks_no_crash(s):
    try:
        average_marks(s)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"average_marks crashed with: {e!r}"


@given(st.text() | st.none())
def test_parse_srn_no_crash(s):
    try:
        parse_srn(s)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"parse_srn crashed with: {e!r}"


@given(st.text() | st.none())
def test_short_name_no_crash(s):
    try:
        short_name(s)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"short_name crashed with: {e!r}"


# ---------- 2. Valid input must give correct results ----------

@given(st.lists(st.integers(0, 100), min_size=1))
def test_average_marks_valid(marks):
    csv = ",".join(str(m) for m in marks)
    result = average_marks(csv)
    assert result == round(sum(marks) / len(marks), 2)
    assert min(marks) <= result <= max(marks)


srn_strategy = st.builds(
    lambda c, y, d, n: f"PES{c}UG{y:02d}{d}{n:03d}",
    st.integers(0, 9),
    st.integers(0, 99),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    st.integers(0, 999),
)


@given(srn_strategy)
def test_parse_srn_valid(srn):
    campus, year, dept = parse_srn(srn)
    assert campus == srn[:4]
    assert year == int(srn[6:8])
    assert dept == srn[8:10]


@given(st.text(alphabet=LOWER, min_size=1), st.text(alphabet=LOWER, min_size=1))
def test_short_name_valid(first, last):
    result = short_name(f"{first} {last}")
    assert result == first[0].upper() + ". " + last.capitalize()


# ---------- 3. Invalid input must be rejected with ValueError ----------

@given(
    st.lists(st.integers(0, 100)),
    st.one_of(st.integers(max_value=-1), st.integers(min_value=101)),
)
def test_average_marks_rejects_out_of_range(valid, bad):
    csv = ",".join(str(m) for m in valid + [bad])
    with pytest.raises(ValueError):
        average_marks(csv)


@pytest.mark.parametrize("bad", ["", " ", ",", "1,,3", "one,two", "78,85,", "1.5,2"])
def test_average_marks_rejects_malformed(bad):
    with pytest.raises(ValueError):
        average_marks(bad)


@given(st.text())
def test_parse_srn_rejects_invalid_format(s):
    assume(not re.fullmatch(SRN_PATTERN, s))
    with pytest.raises(ValueError):
        parse_srn(s)


@given(st.text())
def test_short_name_rejects_wrong_word_count(s):
    assume(len(s.split()) != 2)
    with pytest.raises(ValueError):
        short_name(s)

@given(st.from_regex(r"[A-Z]{6}[0-9]{2}[A-Z0-9]{2,5}", fullmatch=True))
def test_parse_srn_rejects_wrong_prefix(s):
    # Looks SRN-like (digits at positions 6-7) but never starts with PES<digit>UG
    with pytest.raises(ValueError):
        parse_srn(s)