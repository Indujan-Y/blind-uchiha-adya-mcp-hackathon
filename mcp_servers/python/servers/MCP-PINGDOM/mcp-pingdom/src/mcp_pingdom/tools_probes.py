import httpx
from typing import Any, Dict
import logging
logging.basicConfig(filename='stdio_server_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

PINGDOM_API_BASE = "https://api.pingdom.com/api/3.1"

def get_all_probes(args: dict = None) -> dict:
    logging.debug(f"get_all_probes args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_all_probes creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/probes"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_all_probes successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_all_probes: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False} 