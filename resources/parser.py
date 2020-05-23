from flask_restful import Resource
import requests
import json

from baikz import ParseExchenge


class Parser(Resource):
    @classmethod
    def get(cls):
        parse_data = ParseExchenge.start_parse()

        url = 'http://78.155.206.12/items'
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'}
        # data = {"user_info": [{"username": "<user login>",
        #                        "key": "<api_key>"},
        #                       {}]}
        response = requests.post(url, data=json.dumps(parse_data), headers=headers)
        print(response.status_code)

        if response.status_code == 201:
            return {'message': 'Success!'}
        return {'message': 'An error has occurred.'}
