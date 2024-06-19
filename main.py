import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Path to the google-ads.yaml file
config_path = os.path.join(os.path.dirname(__file__), 'google-ads.yaml')

# Initialize the Google Ads API client
client = GoogleAdsClient.load_from_storage(path=config_path, version="v17")

# Get the customer ID from the configuration
customer_id = client.login_customer_id

def print_bakery_data(client, customer_id, location_id):
    # Create a query to fetch data for bakeries in Dallas
    query_campaign = (
        f"SELECT campaign.name FROM campaign "
        f"WHERE campaign.status = 'ENABLED' "
        f"AND campaign.name LIKE '%bakery%'"
    )

    query_ad_group = (
        f"SELECT ad_group.name FROM ad_group "
        f"WHERE ad_group.status = 'ENABLED' "
        f"AND ad_group.name LIKE '%bakery%'"
    )

    # Issue a request to the Google Ads API for campaigns
    try:
        google_ads_service = client.get_service("GoogleAdsService")
        response_campaign = google_ads_service.search(customer_id=customer_id, query=query_campaign)
        for row in response_campaign:
            campaign_name = row.campaign.name
            print(f"Campaign: {campaign_name}")
    except GoogleAdsException as ex:
        print(f'Request for campaigns with ID "{ex.request_id}" failed with status "{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')

    # Issue a request to the Google Ads API for ad groups
    try:
        response_ad_group = google_ads_service.search(customer_id=customer_id, query=query_ad_group)
        for row in response_ad_group:
            ad_group_name = row.ad_group.name
            print(f"Ad Group: {ad_group_name}")
    except GoogleAdsException as ex:
        print(f'Request for ad groups with ID "{ex.request_id}" failed with status "{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')

if __name__ == "__main__":
    location_id = 1023191   # Dallas, TX
    print_bakery_data(client, customer_id, location_id)
