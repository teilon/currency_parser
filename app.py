from flask import Flask
from flask_restful import Api

from resources.parser import Parser

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(Parser, '/parse')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
