from flask import Flask, request, jsonify
from flasgger import swag_from, Swagger
from dotenv import load_dotenv
import collections.abc
import jwt
import os

from flaskr.models.auth import authenticate_route

load_dotenv()

def create_app(test_config = None):
    
    app = Flask(__name__)
    Swagger(app)

    # Task health evaluation
    # https://aws.amazon.com/blogs/containers/a-deep-dive-into-amazon-ecs-task-health-and-task-replacement/
    @app.route('/health')
    def health() -> Flask.response_class:
        health = { 'exit_code': 0 }
        return jsonify(health), 200

    @app.post('/authenticate')
    @swag_from('specs/authenticate.yml', validation=True)
    def authenticate() -> Flask.response_class:
        data = request.get_json()
        token = jwt.encode(data['user_data'], os.getenv('SECRET_KEY', 'test-key'), algorithm = 'HS256')
        return jsonify({ 'authorization': token }), 201

    # POST method: submit data to the server,
    # process that data and return a new value.
    @app.post('/calculate')
    @authenticate_route
    @swag_from('specs/calculate.yml', validation=True)
    def calculate() -> Flask.response_class:
        # parse JSON from the request
        request_data = request.get_json()
        flights: list = request_data['flights']
        
        # openApi has verified 'data' is a list,
        # validate it is indeed not empty
        # and a list of string unsorted_flights
        if not isinstance(flights, collections.Iterable) or not all(len(f) == 2 for f in flights):
            return jsonify({ 'message': 'Invalid input, should be a valid list' }), 400
        
        # flight exercise here
        try:
            sorted_flights = sort_flights(flights)
        except:
            # the above will throw if not all flights are connected
            return jsonify({ 'message': 'Unable to process the request' }), 422
        
        origin = sorted_flights[0][0]
        destination = sorted_flights[- 1][1]
        result = [origin, destination]
        
        return jsonify(result), 200

    # sort flights
    def sort_flights(unsorted_flights: list) -> list:
        # example request
        # {
        #     "flights": [["SFO", "ATL"], ["ATL", "GSO"], ["IND", "EWR"], ["GSO", "IND"]]
        # }
        # Create an adjacency matrix/list to optimise the search
        adjacency_matrix = { flight[0]: flight for flight in unsorted_flights }
        # i.e. {'SFO': ['SFO', 'ATL'], 'ATL': ['ATL', 'GSO'], 'IND': ['IND', 'EWR'], 'GSO': ['GSO', 'IND']}
        all_origins = set(flight[0] for flight in unsorted_flights)
        # i.e. {'GSO', 'SFO', 'ATL', 'IND'}
        # the first element (origin, in this case 'SFO') does not exist as a destination (flight[1]) in any other flight
        first_flight = all_origins.difference(flight[1] for flight in unsorted_flights)
        # i.e. {'SFO'}
        # pop flights from adjacency matrix
        sorted_flights = [adjacency_matrix.pop(first_flight.pop())]
        # i.e [['SFO', 'ATL']]
        while (adjacency_matrix):
            # one by one, remove the last element from the sorted list
            sorted_flights.append(adjacency_matrix.pop(sorted_flights[-1][1]))
        return sorted_flights
    
    return app

if __name__ == '__main__':
    create_app().run()