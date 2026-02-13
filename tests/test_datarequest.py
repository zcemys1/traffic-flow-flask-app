import pytest
from traffic_app_flask import create_app  
import os

@pytest.fixture
def client():

    test_config = {
        'SECRET_KEY': 'test_secret_key',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': False,
        'TESTING': True,  
    }
    

    app = create_app(test_config)
    

    with app.test_client() as client:
        yield client

def test_datarequest_page_load(client):
    """
    GIVEN the /data_request/ page is loaded
    WHEN a GET request is made to the page
    THEN the page should load successfully
    """
    response = client.get('/data_request/')
    

    assert response.status_code == 200
    
   
    assert b"Traffic Data Request" in response.data  
    assert b"Select Borough" in response.data 
    assert b"Select Year" in response.data  
    

def test_valid_form_submission(client, tmp_path):
    """
    GIVEN the /data_request/ page with valid form data
    WHEN the form is submitted with a valid borough and year
    THEN the CSV file should be generated and downloaded
    """


    data = {
        'borough': '7',#camden
        'year': '2023', 
        'vehicle_type': 'cars', 
    }
    response = client.post('/data_request/', data=data)

    assert response.status_code == 200

    expected_file_path = r'C:\Users\uswe\OneDrive - University College London\Desktop\COMP0034 T2 2025\comp0034-cw2-zcemys1\traffic_data.csv'
    assert os.path.exists(expected_file_path)

    with open(expected_file_path, 'r') as f:
        csv_content = f.read()
        
        assert 'year' in csv_content 
        assert 'borough_name' in csv_content  
        assert 'cars' in csv_content 
        assert 'all_vehicles' in csv_content  
        
def test_csv_content(client, tmp_path):
    """
    GIVEN the /data_request/ page with valid form data
    WHEN the form is submitted and the CSV is generated
    THEN the CSV should contain the expected data based on the selected borough and year
    """
    data = {
        'borough': '7',  #Camden
        'year': '2023',  
        'vehicle_type': 'cars',  
    }

    expected_file_path = r'C:\Users\uswe\OneDrive - University College London\Desktop\COMP0034 T2 2025\comp0034-cw2-zcemys1\traffic_data.csv'

    client.post('/data_request/', data=data)
    assert os.path.exists(expected_file_path)
    with open(expected_file_path, 'r') as f:
        content = f.readlines()

    assert 'year,borough_name,cars,all_vehicles' in content[0]  
    #this is only specific to camden,2023 and cars
    assert '2023,Camden,313.0,440.6' in content[1]  

        
        
        
def test_back_to_homepage_link(client):
    """
    GIVEN the /data_request/ page is loaded
    WHEN the user visits the page
    THEN the 'Go back to the homepage' link should be present
    """
    
    response = client.get('/data_request/', follow_redirects=True)

    
    assert b'Go back to the homepage' in response.data

