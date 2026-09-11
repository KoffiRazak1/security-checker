import secrets
import string


def generate_password(
    length=16,
    use_lowercase=True,
    use_uppercase=True,
    use_digits=True,
    use_special=True
):
    """
    Génère un mot de passe aléatoire sécurisé.

    La génération utilise le module secrets,
    adapté à la génération de données sensibles.
    """

    if not isinstance(length, int):
        raise TypeError(
            "La longueur doit être un nombre entier."
        )

    if length < 8:
        raise ValueError(
            "La longueur minimale est de 8 caractères."
        )

    if length > 128:
        raise ValueError(
            "La longueur maximale est de 128 caractères."
        )

    character_sets = []

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_digits:
        character_sets.append(string.digits)

    if use_special:
        character_sets.append(
            "!@#$%^&*()-_=+[]{};:,.?/<>"
        )

    if not character_sets:
        raise ValueError(
            "Sélectionnez au moins un type de caractère."
        )

    if length < len(character_sets):
        raise ValueError(
            "La longueur est trop courte pour les options sélectionnées."
        )

    # Un caractère de chaque catégorie sélectionnée
    # garantit que toutes les options choisies sont représentées.
    password_characters = [
        secrets.choice(character_set)
        for character_set in character_sets
    ]

    all_characters = "".join(character_sets)

    # Compléter le reste du mot de passe
    for _ in range(length - len(password_characters)):
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Mélange cryptographiquement sûr
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)