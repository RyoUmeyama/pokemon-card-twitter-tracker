# ポケモンカード Twitter 抽選情報トラッカー

X (旧Twitter) から @pokecamatomeru などのアカウントのポケモンカード抽選情報を自動収集します。

## 🎯 機能

- 指定アカウントのツイートを取得
- 前回実行日時以降のツイートのみを収集
- 抽選関連キーワードで自動フィルタリング
- JSON形式でデータ保存

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

## 📝 今後の拡張予定

- [ ] 複数アカウントの監視
- [ ] ハッシュタグ検索機能
- [ ] GitHub Actions で定期実行
- [ ] 前回実行日時の記録

## 📜 ライセンス

MIT License
