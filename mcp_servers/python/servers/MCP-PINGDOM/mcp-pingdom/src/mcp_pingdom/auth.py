import os
from dotenv import load_dotenv

load_dotenv()

PINGDOM_API_KEY_ENV = "PINGDOM_API_KEY"
PINGDOM_ACCOUNT_EMAIL_ENV = "PINGDOM_ACCOUNT_EMAIL"

class PingdomAuthError(Exception):
    pass

def get_pingdom_api_key() -> str:
    api_key = os.getenv(PINGDOM_API_KEY_ENV)
    if not api_key:
        raise PingdomAuthError(f"Pingdom API key not found. Please set the {PINGDOM_API_KEY_ENV} environment variable.")
    return api_key

def get_pingdom_account_email() -> str:
    email = os.getenv(PINGDOM_ACCOUNT_EMAIL_ENV)
    if not email:
        raise PingdomAuthError(f"Pingdom account email not found. Please set the {PINGDOM_ACCOUNT_EMAIL_ENV} environment variable.")
    return email

def get_auth_headers(creds: dict = None) -> dict:
    """
    Returns Pingdom API headers using provided creds (multi-tenant) or .env fallback (single-tenant).
    """
    if creds:
        api_key = creds.get("api_key")
        account_email = creds.get("account_email")
    else:
        api_key = os.getenv(PINGDOM_API_KEY_ENV)
        account_email = os.getenv(PINGDOM_ACCOUNT_EMAIL_ENV)

    if not api_key or not account_email:
        raise PingdomAuthError("Pingdom API key or account email missing (in creds or .env).")

    return {
        "Authorization": f"Bearer {api_key}",
        "Account-Email": account_email,
        "Accept": "application/json"
    }

