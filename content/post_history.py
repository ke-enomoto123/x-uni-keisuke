"""
投稿履歴管理（重複防止・パターン管理）
logs/post_history.json に記録
"""
import json
import os
from datetime import datetime

HISTORY_FILE = "logs/post_history.json"


def _load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_post(tweet_text: str, topic: str, pattern: str, tweet_id: str = ""):
    os.makedirs("logs", exist_ok=True)
    history = _load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "tweet_id": tweet_id,
        "topic": topic,
        "pattern": pattern,
        "preview": tweet_text[:80],
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_recent_patterns(n: int = 3) -> list:
    history = _load_history()
    return [h["pattern"] for h in history[-n:]]


def get_recent_topics(n: int = 3) -> list:
    history = _load_history()
    return [h["topic"] for h in history[-n:]]


def get_recent_previews(n: int = 100) -> list:
    history = _load_history()
    return [h["preview"] for h in history[-n:]]
