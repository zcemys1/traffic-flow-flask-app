# Copied from Flask documentation: https://flask.palletsprojects.com/en/stable/testing/
import pytest
import sqlite3
#from traffic_app_flask import create_app
from traffic_app_flask import create_app
from traffic_app_flask.database.create_db import add_data, create_db
from playwright.sync_api import sync_playwright

#@pytest.fixture(scope="module")
#def app():
#    app = create_app()
#    #in-memory SQLite database for testing
#    conn = sqlite3.connect(":memory:")
#    cursor = conn.cursor()
#    #initialise database
#    create_db(cursor, conn)
#    add_data(cursor, conn)
#    conn.close()
#    
#    app.config.update({
#        "TESTING": True,
#        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
#    })
# # other setup can go here

  #  yield app

    # clean up / reset resources here
@pytest.fixture(scope="module")
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # In-memory SQLite setup
    with app.app_context():
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        create_db(cursor, conn)
        add_data(cursor, conn)
        conn.close()

        yield app

        # ✅ Clean up SQLAlchemy session
        from traffic_app_flask import db
        db.session.remove()


@pytest.fixture()
def client(app):
    #create a test client using flask application configured for testing
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope="function")
def page():
    """Fixture for Playwright browser page"""
    with sync_playwright() as p:
        # Launch the Chromium browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Yield the page fixture for each test
        yield page
        
        # Cleanup after each test: close the page and browser
        page.close()
        browser.close()
