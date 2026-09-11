from backend.security.password_checker import analyze_password


passwords = [
    "123456",
    "password",
    "Azerty123",
    "MonChien2020!",
    "X7!qP9#vL2@kR8",
]


for password in passwords:

    result = analyze_password(password)

    print("=" * 50)

    print("TEST DU MOT DE PASSE")

    print("Score :", result["score"], "/100")

    print("Niveau :", result["level"])

    print("Longueur :", result["length"])

    print("\nProblèmes :")

    for problem in result["problems"]:
        print(problem)

    print("\nRecommandations :")

    for recommendation in result["recommendations"]:
        print(recommendation)