import httpx
from typing import Any, Dict
import logging
logging.basicConfig(filename='stdio_server_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

PINGDOM_API_BASE = "https://api.pingdom.com/api/3.1"

def get_summary_average(check_id: int, args: dict = None) -> dict:
    logging.debug(f"get_summary_average args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_summary_average creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/summary.average/{check_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_summary_average successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_summary_average: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def get_summary_outage(check_id: int, args: dict = None) -> dict:
    logging.debug(f"get_summary_outage args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_summary_outage creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/summary.outage/{check_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_summary_outage successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_summary_outage: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def get_summary_performance(check_id: int, args: dict = None) -> dict:
    logging.debug(f"get_summary_performance args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_summary_performance creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/summary.performance/{check_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_summary_performance successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_summary_performance: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False}

def get_summary_pagespeed(check_id: int, args: dict = None) -> dict:
    logging.debug(f"get_summary_pagespeed args: {args}")
    creds = args.get("__credentials__", {}) if args else {}
    logging.debug(f"get_summary_pagespeed creds present: {'PINGDOM_API_KEY' in creds and 'PINGDOM_ACCOUNT_EMAIL' in creds}")
    if not creds.get("PINGDOM_API_KEY") or not creds.get("PINGDOM_ACCOUNT_EMAIL"):
        logging.error("Pingdom API key or account email missing in request.")
        return {"data": None, "error": "Pingdom API key or account email missing in request.", "status": False}
    url = f"{PINGDOM_API_BASE}/summary.pagespeed/{check_id}"
    try:
        headers = {
            "Authorization": f"Bearer {creds['PINGDOM_API_KEY']}",
            "Account-Email": creds["PINGDOM_ACCOUNT_EMAIL"]
        }
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("get_summary_pagespeed successful")
            return {"data": response.json(), "error": None, "status": True}
    except Exception as e:
        logging.exception(f"Unexpected error in get_summary_pagespeed: {e}")
        return {"data": None, "error": f"Unexpected error: {str(e)}", "status": False} 