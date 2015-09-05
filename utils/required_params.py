from utils.exceptions import MissingParameter


def check_params(request, required_params):
    for param in required_params:
        if not request.data.get(param, False):
            raise MissingParameter()
