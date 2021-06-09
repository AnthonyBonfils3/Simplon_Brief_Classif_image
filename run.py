#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Fev 01 13:11:37 2021

@author: Bonfils
"""

from api import app
#from api/img_transform import RGB2GrayTransformer, HogTransformer

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, port=5001)