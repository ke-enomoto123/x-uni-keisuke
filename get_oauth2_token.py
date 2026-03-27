"""
X OAuth 2.0 ユーザートークン取得スクリプト（初回のみ実行）
取得したrefresh_tokenをGitHub Secretsに保存してください。
"""
import tweepy

CLIENT_ID = "RUpzQnpZTElmbGpFWExndHlvUHI6MTpjaQ"
CLIENT_SECRET = "ayMsw7w1JLPvPGCpXiAHZf5XJauRkSZbPxV1J4bjOdwrpldIjr"

oauth2_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="https://localhost",
    scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
    client_secret=CLIENT_SECRET,
)

auth_url = oauth2_handler.get_authorization_url()
print("\n" + "="*60)
print("以下のURLをブラウザで開いてください：")
print("="*60)
print(auth_url)
print("="*60)
print("\n認証後、ブラウザのアドレスバーに表示されたURLを")
print("（https://localhost?state=...code=... という形式）")
print("コピーして貼り付けてください：\n")

response_url = input("リダイレクトURL: ").strip()

token = oauth2_handler.fetch_token(response_url)

print("\n" + "="*60)
print("✅ 認証成功！以下をGitHub Secretsに保存してください：")
print("="*60)
print(f"X_OAUTH2_REFRESH_TOKEN = {token.get('refresh_token', 'なし（offline.accessスコープが必要）')}")
print(f"access_token（確認用）= {token.get('access_token', '')[:30]}...")
print("="*60)
