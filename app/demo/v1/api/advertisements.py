# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from json import dumps
from ..regression import adver
class Advertisements(Resource):

    def get(self):
        
        result = adver.main()
        output = list()
        # print(result)
        for key, value in result.items():
            # print(key, value)
            value['factor'] = key
            output.append(value)
        return output, 200, None