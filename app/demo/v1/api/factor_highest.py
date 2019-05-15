# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from ..regression import adver

class FactorHighest(Resource):

    def get(self):
        result = adver.main() # ! Do NOT change this part
        # TODO: put your filtering logic

        # TODO formating the output
        msg = ''
        answer = ''
        # ! Do NOT change this part
        return {'messages':[{'text':msg + answer }]}, 200, None