import os

import requests
from dotenv import load_dotenv


load_dotenv()


HIBP_API_URL = (
    "https://haveibeenpwned.com/api/v3/breachedaccount"
)


# ============================================================
# CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 10
MAX_EMAIL_LENGTH = 254


# ============================================================
# VALIDATION EMAIL
# ============================================================

def is_valid_email(email):
    """
    Vérifie simplement le format d'une adresse e-mail.
    """

    if not isinstance(email, str):
        return False

    email = email.strip()

    if not email:
        return False

    if len(email) > MAX_EMAIL_LENGTH:
        return False

    parts = email.rsplit("@", 1)

    if len(parts) != 2:
        return False

    local_part, domain = parts

    if not local_part or not domain:
        return False

    if " " in email:
        return False

    if "." not in domain:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return True


# ============================================================
# EMAIL BREACH CHECKER
# ============================================================

def check_email_breach(email):
    """
    Vérifie si une adresse e-mail apparaît dans
    les violations de données connues par HIBP.

    Sécurité :
    - aucune sauvegarde locale de l'adresse ;
    - aucune écriture dans les logs ;
    - clé API uniquement récupérée depuis .env ;
    - timeout réseau ;
    - erreurs réseau transformées en erreurs génériques.
    """

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not isinstance(email, str):
        raise TypeError(
            "L'adresse e-mail doit être une chaîne de caractères."
        )

    email = email.strip()

    if not email:
        raise ValueError(
            "L'adresse e-mail ne peut pas être vide."
        )

    if not is_valid_email(email):
        raise ValueError(
            "L'adresse e-mail n'est pas valide."
        )

    # --------------------------------------------------------
    # CLÉ API
    # --------------------------------------------------------

    api_key = os.getenv("HIBP_API_KEY")

    if not api_key:
        raise RuntimeError(
            "La clé API HIBP n'est pas configurée."
        )

    # --------------------------------------------------------
    # REQUÊTE HIBP
    # --------------------------------------------------------

    try:

        response = requests.get(
            HIBP_API_URL,
            params={
                "truncateResponse": "true"
            },
            headers={
                "hibp-api-key": api_key,
                "user-agent": (
                    "Password-Email-Security-Checker"
                )
            },
            timeout=REQUEST_TIMEOUT
        )

    except requests.exceptions.Timeout as error:

        raise RuntimeError(
            "Le service HIBP a mis trop de temps à répondre."
        ) from error

    except requests.exceptions.ConnectionError as error:

        raise RuntimeError(
            "Impossible de contacter le service HIBP."
        ) from error

    except requests.exceptions.RequestException as error:

        raise RuntimeError(
            "Une erreur réseau est survenue avec HIBP."
        ) from error

    # --------------------------------------------------------
    # RÉPONSE HIBP
    # --------------------------------------------------------

    if response.status_code == 404:

        return {
            "found": False,
            "breaches": []
        }

    if response.status_code == 401:

        raise RuntimeError(
            "La clé API HIBP est invalide ou non autorisée."
        )

    if response.status_code == 403:

        raise RuntimeError(
            "La requête vers HIBP n'est pas autorisée."
        )

    if response.status_code == 429:

        raise RuntimeError(
            "Trop de requêtes vers HIBP. Réessayez plus tard."
        )

    try:

        response.raise_for_status()

    except requests.exceptions.HTTPError as error:

        raise RuntimeError(
            "Le service HIBP a retourné une erreur."
        ) from error

    # --------------------------------------------------------
    # LECTURE DU JSON
    # --------------------------------------------------------

    try:

        breaches = response.json()

    except ValueError as error:

        raise RuntimeError(
            "La réponse du service HIBP est invalide."
        ) from error

    if not isinstance(breaches, list):

        raise RuntimeError(
            "La réponse du service HIBP est inattendue."
        )

    # --------------------------------------------------------
    # EXTRACTION DES INFORMATIONS
    # --------------------------------------------------------

    results = []

    for breach in breaches:

        if not isinstance(breach, dict):
            continue

        results.append({
            "name": breach.get("Name"),
            "title": breach.get("Title"),
            "domain": breach.get("Domain"),
            "breach_date": breach.get("BreachDate"),
            "data_classes": breach.get(
                "DataClasses",
                []
            )
        })

    return {
        "found": len(results) > 0,
        "breaches": results
    }