from datetime import datetime

def calculate_age(dob):
    if isinstance(dob, datetime):
        today = datetime.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return None

def is_adult(age):
    return age is not None and age >= 18
