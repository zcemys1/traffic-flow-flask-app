import pytest
from traffic_app_flask import create_app
from flask.testing import FlaskClient
from traffic_app_flask.models import Borough

@pytest.fixture
def client():
    app = create_app()  
    with app.test_client() as client:
        yield client
#        
def test_borough_selection_form(client: FlaskClient):
    """
    GIVEN the /flow/ page is loaded
    WHEN the user selects a borough and submits the form
    THEN traffic data for the selected borough should be displayed
    """
    response = client.post('/flow/', data={
        'borough': 7,
    })
    assert response.status_code == 200 
    assert b'Camden' in response.data
  
def test_display_traffic_data(client: FlaskClient):
    """
    GIVEN the /flow/ page is loaded with a borough selected
    WHEN the traffic data for the borough exists
    THEN the traffic data table should be displayed
    """
    response = client.get('/flow/')
    assert b'Select a year' in response.data  
    assert b'Cars' in response.data  
    assert b'All Vehicles' in response.data 
    
    
def test_display_historic_data(client: FlaskClient):
    """
    GIVEN the user has selected a year and vehicle type
    WHEN the historic data for the selected year and vehicle type is available
    THEN the historic traffic data should be displayed
    """
    response = client.post('/flow/', data={
        'year': '1993', 
        'vehicle_type': 'cars', 
        'borough_id': '7',  
        'historic_submit': '1'
    })
    assert b'Historic Traffic Data' in response.data
    assert b'1993' in response.data
    assert b'million vehicle kilometres' in response.data 

def test_invalid_borough_id_submission(client: FlaskClient):
    """
    GIVEN the user submits a historic request with no data
    WHEN borough_id is valid but no data is found
    THEN a "No data found" message should be displayed
    """
    response = client.post('/flow/', data={
        'year': '1800',  # a year that doesn’t exist
        'vehicle_type': 'cars',
        'borough_id': '7',  # a valid borough ID
        'historic_submit': '1'
    })

    assert response.status_code == 200
    assert b'No data found' in response.data

def test_back_to_homepage_link(client: FlaskClient):
    """
    GIVEN the /flow page is loaded
    WHEN the user visits the page
    THEN the 'Go back to the homepage' link should be present
    """
    
    response = client.get('/flow', follow_redirects=True)

    
    assert b'Go back to the homepage' in response.data
