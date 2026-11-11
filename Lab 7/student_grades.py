import re

SRN_PATTERN = re.compile(r"PES[0-9]UG[0-9]{2}[A-Z]{2}[0-9]{3}")


def average_marks(marks_csv):
    if not isinstance(marks_csv, str):
        raise ValueError("marks must be given as a comma-separated string")
    parts = [p.strip() for p in marks_csv.split(',')]
    marks = []
    for p in parts:
        if not re.fullmatch(r"[0-9]+", p):
            raise ValueError(f"invalid mark: {p!r} (use whole numbers like 78,85,92)")
        value = int(p)
        if value > 100:
            raise ValueError(f"mark out of range (0-100): {value}")
        marks.append(value)
    return round(sum(marks) / len(marks), 2)


def parse_srn(srn):
    if not isinstance(srn, str):
        raise ValueError("SRN must be a string")
    if not SRN_PATTERN.fullmatch(srn):
        raise ValueError("invalid SRN format (expected e.g. PES1UG23CS123)")
    return srn[:4], int(srn[6:8]), srn[8:10]


def short_name(full_name):
    if not isinstance(full_name, str):
        raise ValueError("name must be a string")
    parts = full_name.split()
    if len(parts) != 2:
        raise ValueError("enter exactly two words: first and last name")
    first, last = parts
    return first[0].upper() + ". " + last.capitalize()


def main():
    print("==== Running average_marks ====")
    user_input = input("Enter marks as CSV (e.g. 78,85,92): ")
    try:
        result = average_marks(user_input)
        print("Average Marks:", result)
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running parse_srn ====")
    user_input = input("Enter an SRN (e.g. PES1UG23CS123): ")
    try:
        result = parse_srn(user_input)
        print("Campus, Year and Dept:", result)
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running short_name ====")
    user_input = input("Enter first and last name (e.g. ravi kumar): ")
    try:
        result = short_name(user_input)
        print("Short Name:", result)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()