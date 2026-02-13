# Copied from Flask documentation: https://flask.palletsprojects.com/en/stable/testing/
import pytest
from traffic_app_flask import create_app
from traffic_app_flask.routes import db
import os


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

#index route 
def test_index(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Where are you trying to go?' in response.data

#dashboard route:
def test_dashboard(client):
    """Test the dashboard route"""
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'What is ULEZ?' in response.data  #check heading

#ulez check route
def test_ulez_check(client):
    """Test the ULEZ check route for GET and POST"""
    #test GET request
    response = client.get('/ulez_check/')
    assert response.status_code == 200
    assert b'Check your vehicle compliancy' in response.data  # check page heading

    #test POST request
    response = client.post('/ulez_check/', data={
        'fuel_type': 'Petrol',
        'year': '2006',
    })
    assert response.status_code == 200
    assert b'Your vehicle is ULEZ compliant.' in response.data  

#flow route
def test_flow(client, app):
    with app.app_context():
    

        # GET request to load the page
        response = client.get('/flow/')
        assert response.status_code == 200

        data = {
            'year': 2020, 
            'vehicle_type': 'cars',
            'borough_id': 10, 
            'historic_submit': '1',
        }
        #POST Request
        response = client.post('/flow/', data=data)
        assert response.status_code == 200

        assert b'Historic Traffic Data' in response.data
        db.session.remove()

        db.engine.dispose()

        

#data request 

def test_data_request(client):
    """Test the data request route for GET and POST"""
    csv_file_path = 'traffic_data.csv'
    # Test GET request
    response = client.get('/data_request/')
    print(response.data)
    assert response.status_code == 200
    assert b'Enter your preferences below:' in response.data 

    # Test POST request with form submission
    response = client.post('/data_request/', data={
        'borough': 'Enfield',  
        'year': '2020',
        'vehicle_type': 'cars',
    })
    assert response.status_code == 200
    assert os.path.exists(csv_file_path)
    


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()