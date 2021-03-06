# -*- coding: utf-8 -*-
"""
Execute some code in a sandboxed environnment
"""
from __future__ import division

from datetime import datetime, timedelta
from django.db.models import Q
import random
from bois.scripts.random import *
from vomito.models import *
from vomito.scripts import *

DEFAULT_STATUS = "ok"


class StopScript(Exception):
    """
    Class to emulate a "return" in the eval'd code.
    """
    message = ""

    def __init__(self, message):
        self.message = message
        super(StopScript, self).__init__()


def stop(status=""):
    """
    Stop script execution right now.
    """
    raise StopScript(status)


def execute(code, param=None, context=None, filename='<string>'):
    """
    Runs the specified code, with access to specified context.

    param is the param to be used in the script, it will be returned when specified.

    context indicates additional contexts you want to give to the scripter.

    filename is the name that will be displayed in the stacktrace.
    """

    status = 'ok'

    # Import context
    if context is not None:
        l = locals()
        for k, v in context.items():
            l[k] = v

    if code is not None:
        try:
            exec(compile(code, filename, 'exec'))
        except StopScript as ss:
            if ss.message != "":
                status = ss.message
            pass

    return status, param
