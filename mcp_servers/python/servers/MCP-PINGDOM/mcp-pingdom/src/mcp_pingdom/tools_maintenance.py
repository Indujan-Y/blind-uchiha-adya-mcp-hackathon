import httpx
from typing import Any, Dict
import logging
logging.basicConfig(filename='stdio_server_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

PINGDOM_API_BASE = "https://api.pingdom.com/api/3.1"

def get_all_maintenance(args: dict = None) -> dict:
    logging.debug(f"get_all_maintenance args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_all_maintenance creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/maintenance"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def create_maintenance(maintenance_data: dict, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"create_maintenance args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"create_maintenance creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/maintenance"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.post(url, data=maintenance_data, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except httpx.HTTPStatusError as e:
        try:
            error_msg = e.response.json().get("error", {}).get("errormessage", e.response.text)
        except Exception:
            error_msg = e.response.text
        return {"data": None, "error": f"Pingdom API error: {error_msg}", "status": False}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def update_maintenance(maintenanceid: int, update_data: dict, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"update_maintenance args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"update_maintenance creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/maintenance/{maintenanceid}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.put(url, data=update_data, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except httpx.HTTPStatusError as e:
        try:
            error_msg = e.response.json().get("error", {}).get("errormessage", e.response.text)
        except Exception:
            error_msg = e.response.text
        return {"data": None, "error": f"Pingdom API error: {error_msg}", "status": False}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def delete_maintenance(maintenanceid: int, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"delete_maintenance args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"delete_maintenance creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/maintenance/{maintenanceid}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.delete(url, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except httpx.HTTPStatusError as e:
        try:
            error_msg = e.response.json().get("error", {}).get("errormessage", e.response.text)
        except Exception:
            error_msg = e.response.text
        return {"data": None, "error": f"Pingdom API error: {error_msg}", "status": False}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False} 