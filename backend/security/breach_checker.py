import hashlib
import requests


HIBP_API_URL = "https://api.pwnedpasswords.com/range/"


def check_password_breach(password):
    """
    Vérifie si un mot de passe apparaît dans des fuites connues.

    Sécurité :
    - Le mot de passe complet reste local.
    - SHA-1 est calculé localement.
    - Seuls les 5 premiers caractères du hash sont envoyés à HIBP.
    - La comparaison du suffixe est effectuée localement.
    """

    if not isinstance(password, str):
        raise TypeError(
            "Le mot de passe doit être une chaîne de caractères."
        )

    if not password:
        raise ValueError(
            "Le mot de passe ne peut pas être vide."
        )

    # SHA-1 calculé LOCALLEMENT
    sha1_hash = hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()

    # Seulement les 5 premiers caractères sont envoyés
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    response = requests.get(
        HIBP_API_URL + prefix,
        headers={
            "Add-Padding": "true",
            "User-Agent": "Password-Security-Checker"
        },
        timeout=10
    )

    response.raise_for_status()

    # Comparaison locale
    for line in response.text.splitlines():
        parts = line.split(":")

        if len(parts) != 2:
            continue

        returned_suffix = parts[0].strip().upper()
        count = int(parts[1].strip())

        if returned_suffix == suffix:
            return {
                "pwned": True,
                "count": count
            }

    return {
        "pwned": False,
        "count": 0
    }