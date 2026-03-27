"""
X（Twitter）自動投稿メインスクリプト
"""
import json
import os
from datetime import datetime

from content.caption_generator import build_tweet
from content.post_history import save_post
from x.poster import post_tweet


def main():
    print("=" * 50)
    print(f"[Main] X自動投稿開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # ツイート生成
    result = build_tweet()
    tweet_text = result["tweet_text"]
    topic = result["topic"]
    pattern = result["pattern"]
    score = result["score"]

    print(f"\n[Main] ===== 生成されたツイート =====")
    print(tweet_text)
    print(f"[Main] 文字数: {len(tweet_text)}/280")
    print(f"[Main] スコア: {score:.1f}/10.0")
    print("=" * 40)

    # X に投稿
    tweet_id = post_tweet(tweet_text)

    # 履歴保存
    save_post(tweet_text, topic, pattern, tweet_id)

    # ログ保存
    os.makedirs("logs", exist_ok=True)
    log = {
        "timestamp": datetime.now().isoformat(),
        "tweet_id": tweet_id,
        "topic": topic,
        "pattern": pattern,
        "score": score,
        "tweet_text": tweet_text,
        "char_count": len(tweet_text),
    }
    with open("logs/latest_post.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"\n[Main] 完了! ログ保存: logs/latest_post.json")


if __name__ == "__main__":
    main()
