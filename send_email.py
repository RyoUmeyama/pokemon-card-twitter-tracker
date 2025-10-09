"""
ポケモンカード抽選情報をメールで通知
"""
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path


def load_tweets(filename):
    """JSONファイルからツイートを読み込み"""
    filepath = Path(filename)
    if not filepath.exists():
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_email_body(tweets):
    """メール本文を作成"""
    if not tweets:
        return "本日は新しい抽選情報はありませんでした。"

    body = f"ポケモンカード抽選情報 ({len(tweets)}件)\n"
    body += f"取得日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    body += "=" * 60 + "\n\n"

    for i, tweet in enumerate(tweets[:20], 1):  # 最大20件
        body += f"【{i}】\n"
        body += f"投稿者: @{tweet.get('username', 'unknown')}\n"
        body += f"日時: {tweet['created_at']}\n"
        body += f"内容:\n{tweet['text']}\n\n"
        body += f"URL: {tweet['url']}\n"
        body += f"いいね: {tweet['likes']}  リツイート: {tweet['retweets']}\n"
        body += "-" * 60 + "\n\n"

    if len(tweets) > 20:
        body += f"\n※ 他 {len(tweets) - 20}件の抽選情報があります\n"

    return body


def send_email(subject, body):
    """メールを送信"""
    # SMTP設定を環境変数から取得
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    if not all([smtp_server, smtp_username, smtp_password, recipient_email]):
        print("❌ SMTP設定が不足しています")
        return False

    try:
        # メールメッセージを作成
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # SMTPサーバーに接続して送信
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        print(f"✅ メール送信成功: {recipient_email}")
        return True

    except Exception as e:
        print(f"❌ メール送信エラー: {e}")
        return False


def main():
    """メイン処理"""
    print("=" * 60)
    print("ポケモンカード抽選情報 メール通知")
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 統合結果を読み込み
    tweets = load_tweets('all_lottery_tweets.json')

    if not tweets:
        # ファイルが存在しない場合は個別ファイルを確認
        user_tweets = load_tweets('pokecamatomeru_tweets.json')
        hashtag_tweets = load_tweets('hashtag_tweets.json')
        tweets = user_tweets + hashtag_tweets

    print(f"📧 {len(tweets)}件の抽選情報を通知します")

    # メール本文を作成
    body = create_email_body(tweets)

    # メールを送信
    subject = f"【ポケモンカード】抽選情報 ({len(tweets)}件) - {datetime.now().strftime('%Y/%m/%d')}"

    if send_email(subject, body):
        print("✅ 通知完了")
    else:
        print("❌ 通知失敗")


if __name__ == '__main__':
    main()
