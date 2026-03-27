import tweepy
from config import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET, X_BEARER_TOKEN


def post_tweet(text: str) -> str:
    """
    X（Twitter）にツイートを投稿する。
    OAuth 1.0a を使用。
    Returns: tweet_id
    """
    print(f"[X] ツイート投稿開始...")
    print(f"[X] 文字数: {len(text)}")
    print(f"[X] 内容: {text[:60]}...")

    client = tweepy.Client(
        bearer_token=X_BEARER_TOKEN,
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET,
    )

    response = client.create_tweet(text=text)
    tweet_id = str(response.data["id"])
    print(f"[X] 投稿完了! Tweet ID: {tweet_id}")
    print(f"[X] URL: https://x.com/uni_keisuke/status/{tweet_id}")
    return tweet_id
