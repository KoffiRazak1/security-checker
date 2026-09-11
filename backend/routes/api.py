from flask import Blueprint, jsonify, request

from backend.security.password_checker import analyze_password
from backend.security.breach_checker import check_password_breach
from backend.security.email_checker import check_email_breach
from backend.security.password_generator import generate_password


api = Blueprint("api", __name__, url_prefix="/api")


# ==========================================
# LIMITES DE SÉCURITÉ
# ==========================================

MAX_PASSWORD_LENGTH = 256
MAX_EMAIL_LENGTH = 254
MIN_GENERATOR_LENGTH = 8
MAX_GENERATOR_LENGTH = 128


# ==========================================
# OUTIL : VÉRIFIER LE JSON
# ==========================================

def get_json_object():
    """
    Récupère le JSON envoyé par le client.

    Retourne :
        dict : données JSON valides

    Lève :
        ValueError : si les données sont invalides
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValueError(
            "Les données envoyées doivent être un objet JSON."
        )

    return data


# ==========================================
# PASSWORD CHECKER
# ==========================================

@api.post("/password/check")
def check_password():

    try:
        data = get_json_object()

        password = data.get("password")

        # Vérification du type
        if not isinstance(password, str):
            return jsonify({
                "error": "Mot de passe invalide."
            }), 400

        # Vérification du contenu
        if not password:
            return jsonify({
                "error": "Mot de passe manquant."
            }), 400

        # Limitation de taille
        if len(password) > MAX_PASSWORD_LENGTH:
            return jsonify({
                "error": (
                    f"Le mot de passe ne doit pas dépasser "
                    f"{MAX_PASSWORD_LENGTH} caractères."
                )
            }), 400

        # Analyse locale
        result = analyze_password(password)

        # Vérification HIBP avec k-anonymity
        breach_result = check_password_breach(password)

        result["pwned"] = breach_result["pwned"]
        result["breach_count"] = breach_result["count"]

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except TypeError:

        return jsonify({
            "error": "Données invalides."
        }), 400

    except Exception:

        return jsonify({
            "error": (
                "Impossible d'effectuer l'analyse "
                "du mot de passe."
            )
        }), 502


# ==========================================
# EMAIL CHECKER
# ==========================================

@api.post("/email/check")
def check_email():

    try:
        data = get_json_object()

        email = data.get("email")

        # Vérification du type
        if not isinstance(email, str):
            return jsonify({
                "error": "Adresse e-mail invalide."
            }), 400

        # Suppression uniquement des espaces
        # autour de l'adresse
        email = email.strip()

        if not email:
            return jsonify({
                "error": "Adresse e-mail manquante."
            }), 400

        # Limitation de taille
        if len(email) > MAX_EMAIL_LENGTH:
            return jsonify({
                "error": (
                    f"L'adresse e-mail ne doit pas dépasser "
                    f"{MAX_EMAIL_LENGTH} caractères."
                )
            }), 400

        # Vérification auprès du Security Engine
        result = check_email_breach(email)

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except TypeError:

        return jsonify({
            "error": "Données invalides."
        }), 400

    except RuntimeError:

        return jsonify({
            "error": (
                "Le service de vérification "
                "n'est pas correctement configuré."
            )
        }), 500

    except Exception:

        return jsonify({
            "error": (
                "Impossible de vérifier "
                "l'adresse e-mail."
            )
        }), 502


# ==========================================
# PASSWORD GENERATOR
# ==========================================

@api.post("/password/generate")
def generate_password_api():

    try:

        data = request.get_json(silent=True)

        # Le générateur peut fonctionner avec
        # les paramètres par défaut.
        if data is None:
            data = {}

        if not isinstance(data, dict):
            return jsonify({
                "error": "Les données envoyées sont invalides."
            }), 400

        # --------------------------------------
        # LONGUEUR
        # --------------------------------------

        length = data.get("length", 16)

        if isinstance(length, bool) or not isinstance(length, int):
            return jsonify({
                "error": "La longueur doit être un nombre entier."
            }), 400

        if length < MIN_GENERATOR_LENGTH:
            return jsonify({
                "error": (
                    f"La longueur minimale est "
                    f"{MIN_GENERATOR_LENGTH} caractères."
                )
            }), 400

        if length > MAX_GENERATOR_LENGTH:
            return jsonify({
                "error": (
                    f"La longueur maximale est "
                    f"{MAX_GENERATOR_LENGTH} caractères."
                )
            }), 400

        # --------------------------------------
        # OPTIONS DE CARACTÈRES
        # --------------------------------------

        use_lowercase = data.get(
            "use_lowercase",
            True
        )

        use_uppercase = data.get(
            "use_uppercase",
            True
        )

        use_digits = data.get(
            "use_digits",
            True
        )

        use_special = data.get(
            "use_special",
            True
        )

        # Toutes les options doivent être
        # de vrais booléens.
        options = {
            "use_lowercase": use_lowercase,
            "use_uppercase": use_uppercase,
            "use_digits": use_digits,
            "use_special": use_special,
        }

        if not all(
            isinstance(value, bool)
            for value in options.values()
        ):
            return jsonify({
                "error": (
                    "Les options du générateur "
                    "doivent être booléennes."
                )
            }), 400

        # Au moins une catégorie doit être activée.
        if not any(options.values()):
            return jsonify({
                "error": (
                    "Sélectionnez au moins un type "
                    "de caractère."
                )
            }), 400

        # --------------------------------------
        # GÉNÉRATION
        # --------------------------------------

        password = generate_password(
            length=length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special=use_special
        )

        return jsonify({
            "password": password,
            "length": len(password)
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except TypeError:

        return jsonify({
            "error": "Paramètres du générateur invalides."
        }), 400

    except Exception:

        return jsonify({
            "error": (
                "Impossible de générer "
                "le mot de passe."
            )
        }), 500