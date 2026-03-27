import requests
import tweepy
from config import X_OAUTH2_CLIENT_ID, X_OAUTH2_CLIENT_SECRET, X_OAUTH2_REFRESH_TOKEN


def _get_access_token() -> str:
    """リフレッシュトークンを使って新しいアクセストークンを取得"""
    response = requests.post(
        "https://api.x.com/2/oauth2/token",
        auth=(X_OAUTH2_CLIENT_ID, X_OAUTH2_CLIENT_SECRET),
        data={
            "grant_type": "refresh_token",
            "refresh_token": X_OAUTH2_REFRESH_TOKEN,
        },
    )
    if not response.ok:
        print(f"[X] トークン取得エラー: {response.text}")
    response.raise_for_status()
    return response.json()["access_token"]


def post_tweet(text: str) -> str:
    """
    X（Twitter）にツイートを投稿する。
    OAuth 2.0 ユーザーコンテキストを使用。
    Returns: tweet_id
    """
    print(f"[X] ツイート投稿開始...")
    print(f"[X] 文字数: {len(text)}")
    print(f"[X] 内容: {text[:60]}...")

    access_token = _get_access_token()
    print(f"[X] アクセストークン取得完了")

    client = tweepy.Client(access_token=access_token)

    try:
        response = client.create_tweet(text=text)
    except tweepy.errors.Unauthorized as e:
        print(f"[X] 401エラー詳細: {e.response.text}")
        raise
    except tweepy.errors.Forbidden as e:
        print(f"[X] 403エラー詳細: {e.response.text}")
        raise

    tweet_id = str(response.data["id"])
    print(f"[X] 投稿完了! Tweet ID: {tweet_id}")
    print(f"[X] URL: https://x.com/uni_keisuke/status/{tweet_id}")
    return tweet_id
