import httpx
from typing import Any, Dict
import logging
logging.basicConfig(filename='stdio_server_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

PINGDOM_API_BASE = "https://api.pingdom.com/api/3.1"

def get_all_checks(args: dict = None) -> dict:
    logging.debug(f"get_all_checks args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_all_checks creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"https://api.pingdom.com/api/3.1/checks"
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

def get_check_details(check_id: int, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"get_check_details args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_check_details creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/checks/{check_id}"
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

def create_check(check_data: dict = None, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"create_check args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"create_check creds: {creds}")

    # Validate credentials
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {
            "data": None,
            "error": "Pingdom API key or account email missing in request.",
            "status": False,
            "server_message": "❌ Error: Pingdom API key or account email missing in request."
        }

    # Validate check_data
    if not check_data:
        check_data = (
            args.get("check_data")
            or args.get("check")
            or args.get("parameters")
            or {}
        )
        # If still empty, try to extract directly from args if all required fields are present
        required_fields = ["name", "host", "type"]
        if all(field in args for field in required_fields):
            check_data = {field: args[field] for field in required_fields}
    required_fields = ["name", "host", "type"]
    missing = [field for field in required_fields if field not in check_data]
    if missing:
        return {
            "data": None,
            "error": f"Missing required fields in check_data: {', '.join(missing)}",
            "status": False,
            "server_message": f"❌ Error: Missing required fields in check_data: {', '.join(missing)}"
        }

    url = f"{PINGDOM_API_BASE}/checks"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.post(url, data=check_data, headers=headers, timeout=10)
            response.raise_for_status()
            resp_json = response.json()
            # Compose a clear server message for success
            check_info = resp_json.get("check", {})
            check_name = check_info.get("name", check_data.get("name", "(unknown)"))
            check_id = check_info.get("id", "(unknown)")
            server_message = f"✅ Pingdom check '{check_name}' created successfully. ID: {check_id}"
            return {"data": resp_json, "error": None, "status": True, "server_message": server_message}
    except httpx.HTTPStatusError as e:
        # Try to extract error message from Pingdom API
        try:
            error_msg = e.response.json().get("error", {}).get("errormessage", e.response.text)
        except Exception:
            error_msg = str(e)
        return {
            "data": None,
            "error": f"Pingdom API error: {error_msg}",
            "status": False,
            "server_message": f"❌ Error: {error_msg}"
        }
    except Exception as e:
        return {
            "data": None,
            "error": f"Unexpected error: {str(e)}",
            "status": False,
            "server_message": f"❌ Error: Unexpected error: {str(e)}"
        }

def update_check(check_id: int, update_data: dict, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"update_check args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"update_check creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/checks/{check_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.put(url, data=update_data, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def delete_check(check_id: int, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"delete_check args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"delete_check creds: {creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/checks/{check_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.delete(url, headers=headers, timeout=10)
            response.raise_for_status()
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False} 