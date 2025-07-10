import httpx
from mcp_pingdom.auth import get_auth_headers, PingdomAuthError
from typing import Any, Dict

PINGDOM_API_BASE = "https://api.pingdom.com/api/3.1"

def get_check_results(check_id: int, args: dict = None) -> dict:
    print("DEBUG get_check_results args:", args)
    creds = args.get("__credentials__", {}) if args else {}
    print("DEBUG get_check_results creds:", creds)
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/results/{check_id}"
    try:
        headers = get_auth_headers(creds)
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except PingdomAuthError as e:
        return {"data": None, "error": str(e), "status": False}
    except httpx.HTTPStatusError as e:
        try:
            error_msg = e.response.json().get("error", {}).get("errormessage", e.response.text)
        except Exception:
            error_msg = e.response.text
        return {"data": None, "error": f"Pingdom API error: {error_msg}", "status": False}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}
