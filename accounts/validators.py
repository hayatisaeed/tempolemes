from django.core.exceptions import ValidationError

def validate_national_code(national_code):
    if not national_code.isdigit() or len(national_code) != 10:
        raise ValidationError("National code must be exactly 10 digits.")
    
    check_digit = int(national_code[-1])
    sum_digits = sum(int(national_code[i]) * (10 - i) for i in range(9))
    remainder = sum_digits % 11
    
    if (remainder < 2 and check_digit == remainder) or (remainder >= 2 and check_digit == 11 - remainder):
        return True
    else:
        raise ValidationError("Invalid national code.")

def validate_phone_number(phone_number):
    if not phone_number.isdigit() or len(phone_number) != 11:
        raise ValidationError("Phone number must be exactly 11 digits.")
    
    if not phone_number.startswith('09'):
        raise ValidationError("Phone number must start with '09'.")
    
    return True