import anthropic
import random
from difflib import SequenceMatcher

from config import ANTHROPIC_API_KEY, HASHTAGS, TOPIC_CATEGORIES, ACCOUNT_PERSONA
from content.post_patterns import POST_PATTERNS, HOOK_PATTERNS
from content.post_history import get_recent_patterns, get_recent_topics, get_recent_previews

QUALITY_THRESHOLD = 7.0
SIMILARITY_THRESHOLD = 0.65
MAX_RETRIES = 2
X_MAX_CHARS = 280


def select_topic() -> str:
    """直近3件で使ったトピックを避けてランダム選定"""
    recent = get_recent_topics(3)
    available = [t for t in TOPIC_CATEGORIES if t not in recent]
    if not available:
        available = TOPIC_CATEGORIES
    return random.choice(available)


def select_pattern() -> str:
    """直近3件で使ったパターンを避けてランダム選定"""
    recent = get_recent_patterns(3)
    available = [p for p in POST_PATTERNS if p not in recent]
    if not available:
        available = POST_PATTERNS
    return random.choice(available)


def _is_too_similar(text: str, past_previews: list) -> bool:
    """過去100件と類似度が閾値を超えたらTrue"""
    for past in past_previews:
        if SequenceMatcher(None, text[:80], past).ratio() > SIMILARITY_THRESHOLD:
            return True
    return False


def _generate_tweet(topic: str, pattern: str, hook: str, feedback: str = "") -> str:
    """ツイート本文を生成（ハッシュタグなし）"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    feedback_section = f"\n\n【前回の反省点】{feedback}" if feedback else ""

    # 文字数をランダムに決める（短め多め）
    length_type = random.choices(
        ["short", "medium", "long"],
        weights=[40, 35, 25],
        k=1,
    )[0]

    length_instruction = {
        "short": "10〜30文字。つぶやき。一言で刺す",
        "medium": "40〜80文字。日常の気づきを1〜2文で",
        "long": "100〜150文字。体験談やエピソードを短く語る",
    }[length_type]

    prompt = f"""あなたは{ACCOUNT_PERSONA}

今日のテーマ：{topic}
スタイル：{pattern}
書き出しヒント：{hook}{feedback_section}

---

【絶対NG】
- 「〜すべき」「参考にしてください」「モテたいなら〜しなさい」等の説教口調
- カッコつけすぎ（ウイスキー、バー、一人の夜...等の気取った表現）
- 「何もしない」「別にいいか」等のダラけた表現
- 文の最後の「。」は絶対に付けない

【この空気感で書く】
「リモートの日の昼、本気で作る」
「新しい店見つけた日が一番テンション上がる」
「副業3つ目、始めてしまった」
「肌の調子いいと全部うまくいく気がする」
「チームのメンバーに雰囲気変わりましたねって言われた」

---

ルール：
- 文字数：{length_instruction}
- 絵文字は0〜1個、使うなら文末に控えめに
- 自分の体験・気づきを一人称で
- 常に何かに夢中で真剣。仕事も趣味も全力の30代ビジネスマン
- カッコつけないけど、なんか生活が整ってる感
- 具体的な固有名詞や数字を入れるとリアルになる（恵比寿、UNIQLO、3つ目等）
- 文の最後に「。」は絶対に付けない。体言止めか「〜した」「〜だった」で終わる
- ハッシュタグは含めない

本文だけ出力。余計な説明不要。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text.strip()
    text = text.strip('"').strip('\u300c').strip('\u300d')

    # 長さ制限
    max_chars = {"short": 30, "medium": 80, "long": 150}[length_type]
    if len(text) > max_chars * 2:
        for sep in ["。", "\n"]:
            if sep in text[:max_chars + 30]:
                text = text[:text.index(sep)]
                break
        else:
            text = text[:max_chars]
    text = text.rstrip("。")

    return text


def _score_tweet(text: str, topic: str, pattern: str) -> float:
    """品質スコアを数値のみで取得"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""以下のX（Twitter）投稿を採点してください。
アカウントコンセプト：大人の余裕があるモテ男ライフスタイル

投稿文:
{text}

採点基準（各10点満点）：
1. 1行目のフック：最初の一文でスクロールが止まるか
2. 人間味：実際の人が書いたような自然さがあるか
3. 色気・余裕：大人の男の空気感が出ているか
4. 簡潔さ：無駄なく読み切れるか
5. 共感・リプ誘発力：反応・いいねしたくなるか

平均点を小数点1桁の数値のみで返してください。数値以外は不要です。
例: 7.5"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        return float(message.content[0].text.strip())
    except ValueError:
        return 7.0


def build_tweet() -> dict:
    """トピック選定 → 生成 → スコアリング → ハッシュタグ付与"""
    topic = select_topic()
    pattern = select_pattern()
    print(f"[Tweet] トピック: {topic}")
    print(f"[Tweet] パターン: {pattern}")

    past_previews = get_recent_previews(100)
    feedback = ""
    tweet_text = ""
    score = 0.0

    for attempt in range(MAX_RETRIES + 1):
        hook = random.choice(HOOK_PATTERNS).replace("{topic}", topic)

        if attempt > 0:
            print(f"[Tweet] 再生成中... ({attempt}/{MAX_RETRIES})")

        tweet_text = _generate_tweet(topic, pattern, hook, feedback)

        if _is_too_similar(tweet_text, past_previews):
            print("[Tweet] 類似度が高すぎます → 再生成")
            feedback = "過去の投稿と内容が似ているため、全く異なる切り口で書き直してください。"
            continue

        score = _score_tweet(tweet_text, topic, pattern)
        print(f"[Tweet] 品質スコア: {score:.1f}/10.0")

        if score >= QUALITY_THRESHOLD:
            print("[Tweet] 品質チェック通過!")
            break

        print(f"[Tweet] スコア不足 ({score:.1f} < {QUALITY_THRESHOLD}) → 再生成")
        feedback = "1行目のフックが弱い。もっと読者の心を掴む書き出しにしてください。"

    # ハッシュタグを1〜2個だけ追加（280文字に収まる範囲で）
    num_tags = random.choices([0, 1, 2], weights=[20, 50, 30])[0]
    tags = random.sample(HASHTAGS, num_tags) if num_tags > 0 else []
    tags_str = " " + " ".join(tags) if tags else ""

    # 280文字制限チェック
    full_text = tweet_text + tags_str
    if len(full_text) > X_MAX_CHARS:
        full_text = tweet_text[:X_MAX_CHARS - len(tags_str)] + tags_str
    if len(full_text) > X_MAX_CHARS:
        full_text = tweet_text[:X_MAX_CHARS]

    return {
        "topic": topic,
        "pattern": pattern,
        "score": score,
        "tweet_text": full_text,
    }
