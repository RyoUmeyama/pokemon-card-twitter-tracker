# ポケモンカード Twitter 抽選情報トラッカー

X (旧Twitter) から @pokecamatomeru などのアカウントのポケモンカード抽選情報を自動収集します。

## 🎯 機能

- **指定アカウント監視**: @pokecamatomeru などのアカウントからツイート取得
- **ハッシュタグ検索**: (#ポケカ OR #ポケモンカード OR #pokemon OR #ポケモン) AND (#抽選 OR #抽選情報)
- **自動フィルタリング**: 抽選関連キーワードで自動検出
- **GitHub Actions**: 毎日9:00、18:00 JST自動実行
- **メール通知**: 新しい抽選情報が見つかった場合に自動通知
- **JSON形式保存**: 全ツイートデータを保存

## 🔑 セットアップ

### 1. X API認証情報の取得

1. [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) にアクセス
2. プロジェクトとアプリを作成
3. Bearer Token を取得

**必要なAPI権限**
- Read (ツイート読み取り)

**料金プラン**
- Free プラン: 月間1,500ツイート取得まで無料
- Basic プラン: $100/月（月間10,000ツイート）

### 2. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを編集して Bearer Token を設定：
```
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 🚀 使い方

### 基本的な実行

```bash
# @pokecamatomeru の前日からのツイートを取得
python fetch_tweets.py
```

### カスタマイズ

```python
# 特定の日時以降のツイートを取得
from datetime import datetime, timedelta

tweets = fetcher.fetch_user_tweets(
    username='pokecamatomeru',
    since_date=datetime.now() - timedelta(days=7)  # 7日前から
)
```

## 📊 出力データ

`pokecamatomeru_tweets.json` に以下の形式で保存されます：

```json
[
  {
    "id": "1234567890",
    "created_at": "2025-10-09T10:00:00Z",
    "text": "楽天ブックスで「インフェルノX」の抽選受付開始...",
    "likes": 42,
    "retweets": 15,
    "url": "https://twitter.com/pokecamatomeru/status/1234567890",
    "is_lottery_related": true
  }
]
```

## 🔍 抽選関連キーワード

以下のキーワードを含むツイートを自動検出：
- 抽選
- 予約
- 受付
- 販売
- BOX
- パック

## ⚠️ 注意事項

- Twitter API の利用制限に注意してください
- Free プランは月間1,500ツイートまで
- レート制限: 15分あたり900リクエスト

## 📧 GitHub Actions 自動実行

このプロジェクトはGitHub Actionsで自動実行されます。

### 実行スケジュール
- 毎日9:00 JST (00:00 UTC)
- 毎日18:00 JST (09:00 UTC)

### GitHub Secretsの設定

リポジトリの Settings → Secrets and variables → Actions で以下を設定：

- `TWITTER_BEARER_TOKEN`: X API Bearer Token
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_PORT`: 587
- `SMTP_USERNAME`: 送信元メールアドレス
- `SMTP_PASSWORD`: Gmailアプリパスワード
- `RECIPIENT_EMAIL`: 通知先メールアドレス

## 📊 出力ファイル

- `pokecamatomeru_tweets.json`: @pokecamatomeru のツイート
- `hashtag_tweets.json`: ハッシュタグ検索結果
- `all_lottery_tweets.json`: 統合結果（重複除外）

## 📝 今後の拡張予定

- [x] ハッシュタグ検索機能
- [x] GitHub Actions で定期実行
- [x] メール通知機能
- [ ] 複数アカウントの監視
- [ ] Discord/Slack通知

## 📜 ライセンス

MIT License

## 👤 作成者

RyoUmeyama
