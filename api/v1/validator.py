class UserValidator:
    def __init__(self, user):
        self.user = user

    def check_phone_number_value(self):
        if 10 <= len(self.user['phoneNumber']) <= 13:
            return self.user['phoneNumber']
        return 'Invalid'

    def check_passport_url_value(self):
        if len(self.user['passportUrl']) > 0:
            return self.user['passportUrl']
        return 'Invalid'

    def check_password(self):
        if not len(self.user['password']) >= 8:
            return 'Invalid'
        return self.user['password']

    def check_email(self):
        if any(val == "@" for val in self.user['email']):
            if any(val == "." for val in self.user['email']):
                return self.user['email']
            return 'Invalid'
        return 'Invalid'

    def all_checks(self):
        validated_f_name = CheckStrings(self.user['firstname']).check_string()
        validated_l_name = CheckStrings(self.user['lastname']).check_string()
        validated_o_name = CheckStrings(self.user['othername']).check_string()
        validated_pass_url = self.check_passport_url_value()
        validated_phone_no = self.check_phone_number_value()
        validated_email = self.check_email()
        validated_password = self.check_password()
        if 'Invalid' not in [validated_f_name, validated_l_name, validated_o_name,
                             validated_pass_url, validated_email, validated_phone_no,
                             validated_password]:
            return {
                "firstname": validated_f_name,
                "lastname": validated_l_name,
                "othername": validated_o_name,
                "email": validated_email,
                "phoneNumber": validated_phone_no,
                "passportUrl": validated_pass_url,
                "password": validated_password
            }
        return 'Invalid'


class CheckStrings:
    def __init__(self, item):
        self.item = item

    def check_string(self):
        if len(self.item) >= 3 and type(self.item) == str:
            return self.item
        return 'Invalid'


class OfficeValidator:
    pass


class PartyValidator:
    pass
