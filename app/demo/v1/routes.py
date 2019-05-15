# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.factor_highest import FactorHighest
from .api.factor_positive import FactorPositive
from .api.factor_negative import FactorNegative
from .api.suggestion import Suggestion


routes = [
    dict(resource=FactorHighest, urls=['/factor/highest'], endpoint='factor_highest'),
    dict(resource=FactorPositive, urls=['/factor/positive'], endpoint='factor_positive'),
    dict(resource=FactorNegative, urls=['/factor/negative'], endpoint='factor_negative'),
    dict(resource=Suggestion, urls=['/suggestion'], endpoint='suggestion'),
]