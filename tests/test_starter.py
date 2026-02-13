def test_request_example(client):
    response = client.get("/")
    assert response.status_code == 200


#from flask import g
#from traffic_app_flask import db
#import pytest
#from traffic_app_flask import create_app

#@pytest.fixture(scope="function")
#def client():
#    # Create the app with a test config
#    app = create_app('testing')
 #   with app.test_client() as client:
  #      yield client
   #     # Cleanup after the test is finished
    #    db.session.remove()  # Close the session
     #   db.get_engine(app).dispose()  # Dispose the engine to close any open connections
