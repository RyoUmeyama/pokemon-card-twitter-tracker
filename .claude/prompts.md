# Pokemon Card Twitter Tracker - Claude Code Instructions

このプロジェクトは、X (Twitter)からポケモンカード抽選情報を自動収集するシステムです。

## 📋 README更新ルール（重要）

**コードに変更を加えた場合、必ずREADME.mdを更新してください。**

### 更新が必要な場合
- 実行スケジュールの変更
- 監視アカウントの追加・削除
- 検索クエリの変更
- 新機能の追加

### 更新すべきセクション
- `## 🎯 機能`: 実行頻度などの基本情報
- `## 📧 GitHub Actions 自動実行`: スケジュール情報
- `## 📝 今後の拡張予定`: 完了した機能にチェックマーク

## ⚠️ Twitter API制限（重要）

### レート制限
- **月間上限**: 10,000ツイート（Basic v2プラン）
- **15分あたり**:
  - `/users/:id/tweets`: 1,500リクエスト
  - `/tweets/search/recent`: 450リクエスト

### 現在の設定
- **実行頻度**: 1日1回（9:00 JST）
- **取得範囲**: 過去24時間分
- **最大取得数**: 100ツイート/回

### エラー: 429 Too Many Requests
- 原因: レート制限超過
- 対処:
  1. 実行頻度を減らす（推奨: 1日1回）
  2. `max_results`を減らす（100 → 50）
  3. ハッシュタグ検索を無効化

## 📧 メール通知設定

GitHub Secretsで以下を設定:
- `TWITTER_BEARER_TOKEN`: X API Bearer Token
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_PORT`: 587
- `SMTP_USERNAME`: 完全なGmailアドレス（@gmail.com含む）
- `SMTP_PASSWORD`: Gmailアプリパスワード（16文字、スペースなし）
- `RECIPIENT_EMAIL`: 通知先メールアドレス

## 🔍 監視対象

### アカウント
- `@pokecamatomeru`: ポケモンカード抽選情報まとめ

### ハッシュタグ検索クエリ
```
(#ポケカ OR #ポケモンカード OR #pokemon OR #ポケモン) (#抽選 OR #抽選情報) -is:retweet
```

## 📊 出力ファイル

- `pokecamatomeru_tweets.json`: 特定アカウントのツイート
- `hashtag_tweets.json`: ハッシュタグ検索結果
- `all_lottery_tweets.json`: 統合・重複除外後のデータ
