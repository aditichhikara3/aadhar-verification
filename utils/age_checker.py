from datetime import datetime

def calculate_age(dob_str):
    for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
        try:
            dob = datetime.strptime(dob_str, fmt)
            break
        except ValueError:
            continue
    else:
        return None

    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def is_adult(age):
    return age is not None and age >= 18
