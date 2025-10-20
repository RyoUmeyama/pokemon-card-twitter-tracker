# Pokemon Card Twitter Tracker - Claude Code Instructions

⚠️ **重要**: このプロジェクトは `/Users/r.umeyama/work/.claude/CLAUDE.md` の共通ルールに従います。
特に **README更新ルール** と **メール通知設定** を必ず確認してください。

このプロジェクトは、X (Twitter)からポケモンカード抽選情報を自動収集するシステムです。

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

## 🔑 GitHub Secrets設定

### Twitter API
- `TWITTER_BEARER_TOKEN`: X API Bearer Token

### メール通知
メール通知設定の詳細は `/Users/r.umeyama/work/.claude/CLAUDE.md` を参照してください。

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
