import os
from pathlib import Path

from flask import Flask, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from backend.routes.api import api


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

# Limite maximale d'une requête HTTP :
# 16 Ko
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


# Debug désactivé par défaut.
# Pour l'activer localement :
# FLASK_DEBUG=true
DEBUG_MODE = (
    os.getenv("FLASK_DEBUG", "false").lower()
    == "true"
)


# ============================================================
# DOSSIERS DU PROJET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"


# ============================================================
# RATE LIMITING
# ============================================================

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[
        "200 per day",
        "50 per hour",
    ],
    storage_uri="memory://",
)


# ============================================================
# API
# ============================================================

app.register_blueprint(api)


# ============================================================
# HEADERS DE SÉCURITÉ
# ============================================================

@app.after_request
def add_security_headers(response):

    # Protection contre le MIME sniffing
    response.headers["X-Content-Type-Options"] = (
        "nosniff"
    )

    # Empêche l'intégration dans une iframe
    response.headers["X-Frame-Options"] = "DENY"

    # Politique de référent
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    # Limitation des fonctionnalités navigateur
    response.headers["Permissions-Policy"] = (
        "camera=(), "
        "microphone=(), "
        "geolocation=(), "
        "payment=()"
    )

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none';"
    )

    # HSTS uniquement lorsque la connexion est HTTPS
    if request.is_secure:

        response.headers[
            "Strict-Transport-Security"
        ] = (
            "max-age=31536000; "
            "includeSubDomains"
        )

    return response


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# FICHIERS FRONTEND
# ============================================================

@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# ============================================================
# LANCEMENT LOCAL
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=DEBUG_MODE
    )