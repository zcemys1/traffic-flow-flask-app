from flask import url_for
from playwright.sync_api import expect



#loading page up

def test_dashboard_load(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'<iframe' in response.data  
    
#testing if iframe is there    
  
    
def test_iframe_presence(client):
    response = client.get('/dashboard')
    assert b'<iframe' in response.data  

#pytest playwright test

#def test_take_screenshot(live_server, page):
   # page.goto(url_for('dashboard', _external=True))
    
   # page.screenshot(path='screenshots/dash.png')

#testing if main title is rendered correctly 

def test_dashboard_title(client):
    """
    GIVEN the dashboard is loaded
    WHEN the user visits the dashboard
    THEN the title should be present in the page content
    """
    response = client.get('/dashboard')
    assert b'<title> Dashboard 1 </title>' in response.data
    
#testing titles
def test_dashboard_text_one(client):
    response = client.get('/dashboard')
    
    assert b'What is ULEZ?' in response.data
    
#playwritght test:

def test_dashboard_iframe_content(app, page):
    with app.app_context():
        url = url_for("bp.dashboard", _external=True)
        url = url.replace("http://localhost", "http://localhost:5000")

    page.goto(url)
    iframe = page.frame_locator("iframe")  # or use .frame(name="...") if it has one

    # Check for some heading/text inside the iframe
    expect(iframe.locator("h1")).to_have_text("How affective is the Ultra Low Emission Zone?")


    
#def test_dashboard_text_two(client):
  
#    """
#    GIVEN the dashboard is loaded
#    WHEN the user visits the dashboard
#    THEN the text 'What is the impact of the ULEZ zone?' should be present in the iframe content
#    """
#    response = client.get('/dash_app/')
#    assert b'What is the impact of the ULEZ zone?' in response.data   

#def test_dashboard_text_three(client):
#    response = client.get('/dashboard')
#    
#    assert b'Traffic Flow of Cars' in response.data
    
#def test_dashboard_text_four(client):
#    response = client.get('/dashboard')
#    
#    assert b'Traffic Flow of All Vehicles' in response.data
    
#def test_dashboard_text_five(client):
#    response = client.get('/dashboard')
    
#    assert b'What are the prospects for the ULEZ scheme?' in response.data
    



#first image 
#def test_dashboard_image_one_alt(client):
 #   response = client.get('/dashboard')
  #  assert b'London Ultra Low Emission Zone' in response.data 
    
#second image 
#def test_dashboard_image_two_alt(client):
 #   response = client.get('/dashboard')
  #  assert b'Trends in NO in London vs no ULEZ scenario' in response.data   
    
#third image 
#def test_dashboard_image_three_alt(client):
 #   response = client.get('/dashboard')
  #  assert b'ALL ULEZ vehicles (excluding taxis and LEZ vehicles)' in response.data
     
#four image 
#def test_dashboard_image_four_alt(client):
 #   response = client.get('/dashboard')
  #  assert b'PROPOSED LONDON ULEZ EXPANSION FOR 2023' in response.data     

#the dropdown 
     
#def test_dashboard_dropdown_cars_before_ulez(client):
 #   response = client.post('/dashboard', data={'vehicle_type': 'cars'})
  #  assert b'Cars Before ULEZ (Pre-2019)' in response.data 
    
#def test_dashboard_dropdown_cars_within_ulez(client):
 #   response = client.post('/dashboard', data={'vehicle_type': 'cars'})    
  #  assert b'Cars Within ULEZ (2019+)' in response.data 

#def test_dashboard_dropdown_vehicles_before_ulez(client):    
 #   response = client.post('/dashboard', data={'vehicle_type': 'all_vehicles'})
  #  assert b'Vehicles Before ULEZ (Pre-2019)' in response.data
        
#def test_dashboard_dropdown_vehicles_within_ulez(client):
 #   response = client.post('/dashboard', {'vehicle_type': 'all_vehicles'})
  #  assert b'Vehicles Within ULEZ (2019+)' in response.data

#the home button
        
def test_dashboard_back_to_home_button(client):
    response = client.get('/dashboard')
    
    response = client.get('/')
    assert response.status_code == 200


    

  
