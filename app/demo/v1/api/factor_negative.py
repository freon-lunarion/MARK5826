# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from ..regression import adver

class FactorNegative(Resource):

    def get(self):

        result = adver.main()
        # TODO: put your filtering logic
        label = list()
        for key, value in result.items():
            if (value['p'] < 0.05 and value['coefficients'] < 0):
                label.append(key)

        # TODO formating the output
        print(len(label))

        msg = 'The campain had a negative impact in: ' 
        answer = ", ".join(label)

        # ! Do NOT change this part
        return {'messages':[{'text':msg+answer}]}, 200, None