import os
from dotenv import load_dotenv
from account_config import (
    ACCOUNT_NAME,
    ACCOUNT_THEME,
    ACCOUNT_PERSONA,
    TOPIC_CATEGORIES,
    HASHTAGS,
    POST_LANGUAGE,
    POST_TIME,
)

load_dotenv()

# Anthropic (Claude)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# X (Twitter) API OAuth 1.0a
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
X_OAUTH2_CLIENT_ID = "RUpzQnpZTElmbGpFWExndHlvUHI6MTpjaQ"
X_OAUTH2_CLIENT_SECRET = "ayMsw7w1JLPvPGCpXiAHZf5XJauRkSZbPxV1J4bjOdwrpldIjr"
X_OAUTH2_REFRESH_TOKEN = os.getenv("X_OAUTH2_REFRESH_TOKEN")

# account_config の再エクスポート
__all__ = [
    "ANTHROPIC_API_KEY",
    "X_API_KEY",
    "X_API_SECRET",
    "X_ACCESS_TOKEN",
    "X_ACCESS_TOKEN_SECRET",
    "ACCOUNT_NAME",
    "ACCOUNT_THEME",
    "ACCOUNT_PERSONA",
    "TOPIC_CATEGORIES",
    "HASHTAGS",
    "POST_LANGUAGE",
    "POST_TIME",
]
