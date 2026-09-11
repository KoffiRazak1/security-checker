import re

from zxcvbn import zxcvbn


# =========================
# NIVEAU DE SECURITE
# =========================

def get_security_level(score):
    """
    Transforme un score de 0 à 100
    en niveau de sécurité.
    """

    if score <= 20:
        return "Très faible"

    if score <= 40:
        return "Faible"

    if score <= 60:
        return "Moyen"

    if score <= 80:
        return "Fort"

    return "Très fort"


# =========================
# ANALYSE DES CARACTERES
# =========================

def analyze_character_types(password):
    """
    Vérifie les différents types de caractères
    présents dans le mot de passe.
    """

    return {
        "length": len(password),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "digits": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }


# =========================
# MOTS DE PASSE COURANTS
# =========================

COMMON_PASSWORDS = {
    "123456",
    "123456789",
    "password",
    "password123",
    "azerty",
    "qwerty",
    "admin",
    "admin123",
    "12345678",
    "111111",
    "123123",
    "abc123",
}


def detect_common_password(password):
    """
    Détecte quelques mots de passe très courants.
    """

    return password.lower() in COMMON_PASSWORDS


# =========================
# REPETITIONS
# =========================

def detect_repetition(password):
    """
    Détecte des répétitions évidentes.
    Exemple :
    aaaaa
    11111
    !!!!!!
    """

    if len(password) < 3:
        return False

    return bool(re.search(r"(.)\1{2,}", password))


# =========================
# SEQUENCES
# =========================

def detect_sequences(password):
    """
    Détecte quelques séquences simples.
    """

    sequences = [
        "123",
        "234",
        "345",
        "456",
        "567",
        "678",
        "789",
        "abc",
        "bcd",
        "cde",
        "qwerty",
        "azerty",
    ]

    password_lower = password.lower()

    return any(
        sequence in password_lower
        for sequence in sequences
    )


# =========================
# DATES EVIDENTES
# =========================

def detect_obvious_date(password):
    """
    Détecte quelques formats de dates ou années
    facilement reconnaissables.
    """

    # Années comprises entre 1900 et 2099
    if re.search(r"(19\d{2}|20\d{2})", password):
        return True

    # Formats simples :
    # 01/01/2020
    # 01-01-2020
    if re.search(
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
        password
    ):
        return True

    return False


# =========================
# ANALYSE PRINCIPALE
# =========================

def analyze_password(password):
    """
    Analyse un mot de passe localement.

    Le mot de passe n'est pas enregistré,
    écrit dans les logs ou envoyé à un service externe.
    """

    if not isinstance(password, str):
        raise TypeError("Le mot de passe doit être une chaîne de caractères.")

    if not password:
        raise ValueError("Le mot de passe ne peut pas être vide.")

    # Analyse zxcvbn effectuée localement.
    zxcvbn_result = zxcvbn(password)

    # zxcvbn fournit un score de 0 à 4.
    zxcvbn_score = zxcvbn_result["score"]

    # Conversion en score pédagogique de 0 à 100.
    score = zxcvbn_score * 25

    characteristics = analyze_character_types(password)

    problems = []
    recommendations = []


    # =========================
    # LONGUEUR
    # =========================

    if characteristics["length"] < 8:

        problems.append(
            "❌ Mot de passe trop court."
        )

        recommendations.append(
            "Utilisez au minimum une phrase de passe longue et unique."
        )

    elif characteristics["length"] < 12:

        problems.append(
            "⚠️ La longueur pourrait être améliorée."
        )

        recommendations.append(
            "Privilégiez une longueur d'au moins 12 caractères."
        )


    # =========================
    # TYPES DE CARACTERES
    # =========================

    if not characteristics["lowercase"]:

        problems.append(
            "⚠️ Aucune lettre minuscule détectée."
        )

    if not characteristics["uppercase"]:

        problems.append(
            "⚠️ Aucune lettre majuscule détectée."
        )

    if not characteristics["digits"]:

        problems.append(
            "⚠️ Aucun chiffre détecté."
        )

    if not characteristics["special"]:

        problems.append(
            "⚠️ Aucun caractère spécial détecté."
        )


    # =========================
    # MOT DE PASSE COURANT
    # =========================

    if detect_common_password(password):

        problems.append(
            "❌ Mot de passe très courant."
        )

        recommendations.append(
            "Évitez les mots de passe connus et facilement devinables."
        )


    # =========================
    # REPETITIONS
    # =========================

    if detect_repetition(password):

        problems.append(
            "❌ Répétition importante de caractères détectée."
        )

        recommendations.append(
            "Évitez les répétitions prévisibles."
        )


    # =========================
    # SEQUENCES
    # =========================

    if detect_sequences(password):

        problems.append(
            "❌ Séquence prévisible détectée."
        )

        recommendations.append(
            "Évitez les suites comme 123, abc, azerty ou qwerty."
        )


    # =========================
    # DATES
    # =========================

    if detect_obvious_date(password):

        problems.append(
            "⚠️ Une année ou une date facilement identifiable semble présente."
        )

        recommendations.append(
            "Évitez les dates importantes ou facilement devinables."
        )


    # =========================
    # SCORE
    # =========================

    # Si certaines faiblesses évidentes sont détectées,
    # on peut réduire légèrement le score pédagogique.
    penalty = min(len(problems) * 5, 25)

    score = max(0, score - penalty)

    level = get_security_level(score)


    # =========================
    # RECOMMANDATIONS GENERALES
    # =========================

    if len(password) >= 12:

        recommendations.append(
            "Votre longueur est un bon point : conservez une phrase de passe longue et unique."
        )

    recommendations.append(
        "N'utilisez pas le même mot de passe sur plusieurs services."
    )

    recommendations.append(
        "Un gestionnaire de mots de passe peut vous aider à créer et conserver des mots de passe uniques."
    )


    # Éliminer les doublons
    recommendations = list(dict.fromkeys(recommendations))


    # =========================
    # RETOUR
    # =========================

    return {
        "score": score,
        "level": level,
        "problems": problems,
        "recommendations": recommendations,
        "length": characteristics["length"],
        "has_lowercase": characteristics["lowercase"],
        "has_uppercase": characteristics["uppercase"],
        "has_digits": characteristics["digits"],
        "has_special": characteristics["special"],
    }