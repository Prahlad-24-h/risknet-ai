import requests


API_URL = "http://127.0.0.1:8000"


def get_health():
    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def get_customers():
    response = requests.get(
        f"{API_URL}/customers",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_customer(customer_id):
    response = requests.get(
        f"{API_URL}/customer/{customer_id}",
        timeout=10
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()
