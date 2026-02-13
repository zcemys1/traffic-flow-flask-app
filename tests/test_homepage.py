
#loading page up

def test_homepage_load(client):
    """
    GIVEM the home page is loaded
    WHEN the user visits the home page
    THEN the status code should be 200 (OK)
    """
    response = client.get('/')
    assert response.status_code == 200
    
#testing if main title is rendered correctly 

def test_homepage_title(client):
    """
    GIVEN the home page is loaded
    WHEN the user visits the home page
    THEN the title 'ULEZ Analysis' should be present in the page content
    """
    response = client.get('/')
    assert b'ULEZ' in response.data  
    assert b'Analysis' in response.data 

#testing dashboard button links correctly

def test_find_more_traffic_affected_people_redirect(client):
    """Test the 'Find out more about how traffic has affected people' button redirects to the dashboard page"""
    response = client.get('/')
    assert b'Find out more about how traffic has affected people' in response.data
    response = client.get('/dashboard')
    assert response.status_code == 200
    
#testing "check vehicle" button redirects
def test_check_vehicle_redirect(client):
    """Test the 'Check your vehicle' button redirects to the ulezcheck page"""
    response = client.get('/')
    assert b'Check your vehicle' in response.data
    response = client.get('/ulez_check/') 
    assert response.status_code == 200


    
#testing "traffic status" buttons
def test_traffic_status_redirect(client):
    """Test the 'Traffic Status' button redirects to the /flow/ page"""
    response = client.get('/')
    assert b'Traffic Status' in response.data  
    response = client.get('/flow/')  
    assert response.status_code == 200
    
#checking "data request" button
def test_data_request_redirect(client):
    """
    GIVEN the home page is loaded
    WHEN the user clicks on the 'Data Request' button
    THEN the user should be redirected to the '/data_request' page
    """
    response = client.get('/')
    assert b'Data Request' in response.data
    response = client.get('/data_request', follow_redirects=True) 
    assert response.status_code == 200