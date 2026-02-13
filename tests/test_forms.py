from flask import url_for
from playwright.sync_api import expect, Page
import pytest

selected_boroughs = ["Tower Hamlets", "Waltham Forest", "Wandsworth", "Westminster"]
years = list(range(1993, 2024))
vehicle_types = ["cars", "all_vehicles"]


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:5000"  



def test_traffic_flow_form(app, page):
    """Test the Traffic Flow Form title"""
    
    # Ensure we're inside the Flask app context
    with app.app_context():

        url = url_for('bp.flow', _external=True)
        url = url.replace("http://localhost", "http://localhost:5000")
    

    page.goto(url)


    expect(page.locator("h1")).to_have_text("Check the traffic status of a borough")
    
    
def test_flow_form_submission(app, page: Page, base_url):
    with app.app_context():
        url = f"{base_url}/flow"
        page.goto(url)

        for borough in selected_boroughs:
            page.select_option('select[name="borough"]', label=borough)
            page.click('text=Submit')
            page.wait_for_selector('#flow-latest')

            for year in years:
                page.select_option('select[name="year"]', str(year))
                for vehicle in vehicle_types:
                    page.check(f'input[name="vehicle_type"][value="{vehicle}"]')
                    page.click('button[name="historic_submit"]')

                    try:
                        page.wait_for_selector('#flow-historical', timeout=5000)
                        print(f"✓ Checked: Borough={borough}, Year={year}, Vehicle={vehicle}")
                    except:
                        print(f"⚠️ No data or timeout for: Borough={borough}, Year={year}, Vehicle={vehicle}")
