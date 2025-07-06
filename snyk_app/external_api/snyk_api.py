# Module to interact with the SNYK API

import requests
from django.conf import settings


# Logging!
import logging

logger = logging.getLogger(__name__)


def prepare_headers():
    return {
        "Authorization": f"JWT {settings.PROBELY_API_KEY}",
        "Accept": "application/json",
    }


def fetch_findings_page(target_id, page, headers):
    """
    Fetch a given page of findings from Probely API.

    Args:
        target_id (str): The target ID to fetch findings
        page (int): The page number to fetch
        headers (dict): HTTP headers with authentication JWT

    Returns:
        dict | None: The JSON response as dict, or None on failure.
    """
    url = f"{settings.PROBELY_API_BASE_URL}/targets/{target_id}/findings/?page={page}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully fetched page {page} for target {target_id}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"EXCEPTION - failed to fetch page {page} for {target_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"EXCEPTION - {e}")
        return None
