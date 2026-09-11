import requests
from urllib.parse import quote


# ============================================================
# CONFIGURATION
# ============================================================

XPOSEDORNOT_API_URL = (
    "https://api.xposedornot.com/v1/check-email"
)

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
    les violations connues par XposedOrNot.

    Sécurité :
    - aucune sauvegarde locale de l'adresse ;
    - aucune écriture dans les logs ;
    - requête effectuée côté serveur ;
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
    # ENCODAGE DE L'EMAIL
    # --------------------------------------------------------

    encoded_email = quote(email, safe="")

    url = f"{XPOSEDORNOT_API_URL}/{encoded_email}"

    # --------------------------------------------------------
    # REQUÊTE XPOSEDORNOT
    # --------------------------------------------------------

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

    except requests.exceptions.Timeout as error:

        raise RuntimeError(
            "Le service de vérification a mis trop de temps à répondre."
        ) from error

    except requests.exceptions.ConnectionError as error:

        raise RuntimeError(
            "Impossible de contacter le service de vérification."
        ) from error

    except requests.exceptions.RequestException as error:

        raise RuntimeError(
            "Une erreur réseau est survenue pendant la vérification."
        ) from error

    # --------------------------------------------------------
    # RÉPONSE HTTP
    # --------------------------------------------------------

    if response.status_code == 404:

        return {
            "found": False,
            "breaches": []
        }

    if response.status_code == 429:

        raise RuntimeError(
            "Trop de vérifications. Réessayez plus tard."
        )

    try:

        response.raise_for_status()

    except requests.exceptions.HTTPError as error:

        raise RuntimeError(
            "Le service de vérification a retourné une erreur."
        ) from error

    # --------------------------------------------------------
    # LECTURE DU JSON
    # --------------------------------------------------------

    try:

        data = response.json()

    except ValueError as error:

        raise RuntimeError(
            "La réponse du service de vérification est invalide."
        ) from error

    if not isinstance(data, dict):

        raise RuntimeError(
            "La réponse du service de vérification est inattendue."
        )

    # --------------------------------------------------------
    # AUCUNE VIOLATION
    # --------------------------------------------------------

    if data.get("Error") == "Not found":

        return {
            "found": False,
            "breaches": []
        }

    # --------------------------------------------------------
    # VIOLATIONS TROUVÉES
    # --------------------------------------------------------

    raw_breaches = data.get("breaches", [])

    if not isinstance(raw_breaches, list):

        raise RuntimeError(
            "Les données de violation reçues sont invalides."
        )

    results = []

    for breach in raw_breaches:

        # Format XposedOrNot :
        # ["NomDeLaViolation"]

        if isinstance(breach, list) and breach:

            name = breach[0]

        elif isinstance(breach, str):

            name = breach

        else:

            continue

        if not isinstance(name, str):
            continue

        name = name.strip()

        if not name:
            continue

        results.append({
            "name": name,
            "title": None,
            "domain": None,
            "breach_date": None,
            "data_classes": []
        })

    # --------------------------------------------------------
    # RÉSULTAT FINAL
    # --------------------------------------------------------

    return {
        "found": len(results) > 0,
        "breaches": results
    }