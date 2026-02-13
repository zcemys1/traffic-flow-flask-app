from flask.testing import FlaskClient

#import app

#@pytest.fixture
#def client():
#    app = create_app()  
#    with app.test_client() as client:
#        yield client

def test_ulez_check_title(client: FlaskClient):
    """
    GIVEN the /ulez_check page is loaded
    WHEN the user visits the page
    THEN the title 'Check your vehicle compliancy' should be present in the page content
    """
    response = client.get('/ulez_check', follow_redirects=True)
    assert b'Check your vehicle compliancy' in response.data

def test_iframe_presence(client: FlaskClient):
    """
    GIVEN the /ulez_check page is loaded
    WHEN the user visits the page
    THEN the iframe should be present with the correct src
    """
    response = client.get('/ulez_check', follow_redirects=True)
    assert b'<iframe src="https://www.webuyanycar.com/free-car-check/emissions-check/"' in response.data

def test_form_elements(client: FlaskClient):
    """
    GIVEN the /ulez_check page is loaded
    WHEN the user visits the page
    THEN the form should contain the necessary input elements for fuel type and vehicle year
    """
    response = client.get('/ulez_check', follow_redirects=True)
    
    #check radio buttons for fuel type
    assert b'Fuel Type:' in response.data
    assert b'Petrol' in response.data
    assert b'Diesel' in response.data
    assert b'Electric' in response.data
    
    #check dropdown for vehicle registration year
    assert b'Vehicle Registration Year:' in response.data
    for year in range(1990, 2024):
        assert f'<option value="{year}">'.encode() in response.data

def test_submit_functionality(client: FlaskClient):
    """
    GIVEN the form on the /ulez_check page is filled out
    WHEN the user submits the form with valid data
    THEN the ULEZ compliance result should be displayed
    """
    #the form submission
    response = client.post('/ulez_check', data={
        'fuel_type': 'Petrol',
        'year': '2005',
    }, follow_redirects=True)
    
    #check if the result is displayed
    assert b'ULEZ Compliance Result:' in response.data
    assert b'Your vehicle is ULEZ compliant.' in response.data or b'Your vehicle is NOT ULEZ compliant.' in response.data
   
def test_petrol_non_compliant(client: FlaskClient):
    response = client.post('/ulez_check', data={
        'fuel_type': 'Petrol',
        'year': '2004',
    }, follow_redirects=True)
    assert b'Your vehicle is NOT ULEZ compliant.' in response.data
    
def test_diesel_non_compliant(client: FlaskClient):
    response = client.post('/ulez_check', data={
        'fuel_type': 'Diesel',
        'year': '2013',
    }, follow_redirects=True)
    assert b'Your vehicle is NOT ULEZ compliant.' in response.data
    
def test_diesel_compliant(client: FlaskClient):
    response = client.post('/ulez_check', data={
        'fuel_type': 'Diesel',
        'year': '2015',
    }, follow_redirects=True)
    assert b'Your vehicle is ULEZ compliant.' in response.data
    
def test_electric_compliant(client: FlaskClient):
    response = client.post('/ulez_check', data={
        'fuel_type': 'Electric',
        'year': '2020',
    }, follow_redirects=True)
    assert b'Your vehicle is ULEZ compliant.' in response.data

    

#def test_invalid_form_submission(client: FlaskClient):
#    """
#    GIVEN the /ulez_check page is loaded
#    WHEN the user submits the form without selecting a fuel type or vehicle year
#    THEN the form should not be submitted and an appropriate error message should appear
#    """
#    # Submit the form with no data (missing required fields)
#    response = client.post('/ulez_check', data={}, follow_redirects=True)

#    # Check for a redirect instead of a 500 error
#    assert response.status_code == 200  # Ensure that it's not a 500 error

    # Check for the error messages
#    assert b'Please select a fuel type' in response.data or b'Please select a vehicle year' in response.data


def test_back_to_homepage_link(client: FlaskClient):
    """
    GIVEN the /ulez_check page is loaded
    WHEN the user visits the page
    THEN the 'Go back to the homepage' link should be present
    """
    
    response = client.get('/ulez_check', follow_redirects=True)

    
    assert b'Go back to the homepage' in response.data


