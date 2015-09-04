from rest_framework.exceptions import APIException


class MissingParameter(APIException):
    status_code = 409
    default_detail = 'A parameter is missing'
