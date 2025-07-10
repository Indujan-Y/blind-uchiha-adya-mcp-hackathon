import httpx
from typing import Any, Dict
import logging
logging.basicConfig(filename='stdio_server_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

PINGDOM_API_BASE = "https://api.pingdom.com/api/3.1"

def get_all_transactions(args: dict = None) -> dict:
    logging.debug(f"get_all_transactions args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_all_transactions creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/transaction-checks"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_all_transactions successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_all_transactions: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def get_transaction_details(transaction_id: int, args: dict = None) -> dict:
    logging.debug(f"get_transaction_details args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_transaction_details creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/transaction-checks/{transaction_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_transaction_details successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_transaction_details: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def create_transaction(transaction_data: dict, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"create_transaction args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"create_transaction creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/transaction-checks"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.post(url, json=transaction_data, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("create_transaction successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in create_transaction: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def update_transaction(transaction_id: int, update_data: dict, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"update_transaction args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"update_transaction creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/transaction-checks/{transaction_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.put(url, json=update_data, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("update_transaction successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in update_transaction: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def delete_transaction(transaction_id: int, args: dict = None) -> Dict[str, Any]:
    logging.debug(f"delete_transaction args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"delete_transaction creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/transaction-checks/{transaction_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.delete(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("delete_transaction successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in delete_transaction: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False} 