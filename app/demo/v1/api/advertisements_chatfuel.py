# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from json import dumps

class AdvertisementsChatfuel(Resource):

    def get(self):
        # from ..regression import adver
        # result = adver.main()
        print("hello")
        output = {
            'text': 'hello'
        }
        

        return {}, 200, None