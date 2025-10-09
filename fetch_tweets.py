"""
X (旧Twitter) から @pokecamatomeru のポケモンカード抽選情報を取得
"""
import tweepy
import os
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()


class TwitterFetcher:
    def __init__(self):
        """Twitter API認証"""
        # API認証情報を環境変数から取得
        bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

        if not bearer_token:
            raise ValueError("TWITTER_BEARER_TOKEN が設定されていません")

        # Twitter API v2 クライアントを作成
        self.client = tweepy.Client(bearer_token=bearer_token)

    def fetch_user_tweets(self, username, since_date=None):
        """
        指定ユーザーのツイートを取得

        Args:
            username: Twitterユーザー名（@なし）
            since_date: この日時以降のツイートを取得（datetime）
        """
        try:
            # ユーザー情報を取得
            user = self.client.get_user(username=username)
            if not user.data:
                print(f"❌ ユーザー @{username} が見つかりません")
                return []

            user_id = user.data.id
            print(f"✅ ユーザー情報取得: @{username} (ID: {user_id})")

            # since_dateが指定されていない場合は前日から取得
            if since_date is None:
                since_date = datetime.now() - timedelta(days=1)

            # ISO 8601形式に変換
            start_time = since_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            print(f"📅 取得期間: {start_time} 以降")

            # ツイートを取得
            tweets = self.client.get_users_tweets(
                id=user_id,
                start_time=start_time,
                max_results=100,  # 最大100件
                tweet_fields=['created_at', 'text', 'public_metrics'],
                expansions=['referenced_tweets.id']
            )

            if not tweets.data:
                print(f"📭 {start_time} 以降のツイートはありません")
                return []

            # ツイート情報を整形
            results = []
            for tweet in tweets.data:
                tweet_data = {
                    'id': tweet.id,
                    'created_at': tweet.created_at.isoformat(),
                    'text': tweet.text,
                    'likes': tweet.public_metrics['like_count'] if hasattr(tweet, 'public_metrics') else 0,
                    'retweets': tweet.public_metrics['retweet_count'] if hasattr(tweet, 'public_metrics') else 0,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}"
                }

                # 抽選関連キーワードをチェック
                keywords = ['抽選', '予約', '受付', '販売', 'BOX', 'パック']
                if any(keyword in tweet.text for keyword in keywords):
                    tweet_data['is_lottery_related'] = True
                else:
                    tweet_data['is_lottery_related'] = False

                results.append(tweet_data)

            print(f"✅ {len(results)}件のツイートを取得")

            # 抽選関連ツイートの数
            lottery_tweets = [t for t in results if t['is_lottery_related']]
            print(f"🎯 抽選関連ツイート: {len(lottery_tweets)}件")

            return results

        except tweepy.errors.TweepyException as e:
            print(f"❌ Twitter API エラー: {e}")
            return []
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
            return []

    def search_tweets_by_hashtags(self, since_date=None, max_results=100):
        """
        ハッシュタグでツイートを検索
        (#ポケカ OR #ポケモンカード OR #pokemon OR #ポケモン) AND (#抽選 OR #抽選情報)

        Args:
            since_date: この日時以降のツイートを取得（datetime）
            max_results: 取得する最大件数（10-100）
        """
        try:
            # since_dateが指定されていない場合は前日から取得
            if since_date is None:
                since_date = datetime.now() - timedelta(days=1)

            # ISO 8601形式に変換
            start_time = since_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            # 検索クエリを作成
            # (#ポケカ OR #ポケモンカード OR #pokemon OR #ポケモン) AND (#抽選 OR #抽選情報)
            query = "(#ポケカ OR #ポケモンカード OR #pokemon OR #ポケモン) (#抽選 OR #抽選情報) -is:retweet"

            print(f"🔍 検索クエリ: {query}")
            print(f"📅 取得期間: {start_time} 以降")

            # ツイートを検索
            tweets = self.client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=max_results,
                tweet_fields=['created_at', 'text', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username']
            )

            if not tweets.data:
                print(f"📭 {start_time} 以降の該当ツイートはありません")
                return []

            # ユーザー情報を辞書化
            users = {user.id: user.username for user in tweets.includes['users']} if tweets.includes and 'users' in tweets.includes else {}

            # ツイート情報を整形
            results = []
            for tweet in tweets.data:
                username = users.get(tweet.author_id, 'unknown')
                tweet_data = {
                    'id': tweet.id,
                    'created_at': tweet.created_at.isoformat(),
                    'text': tweet.text,
                    'author_id': tweet.author_id,
                    'username': username,
                    'likes': tweet.public_metrics['like_count'] if hasattr(tweet, 'public_metrics') else 0,
                    'retweets': tweet.public_metrics['retweet_count'] if hasattr(tweet, 'public_metrics') else 0,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'is_lottery_related': True  # 検索条件により既に抽選関連
                }
                results.append(tweet_data)

            print(f"✅ {len(results)}件のツイートを取得")

            return results

        except tweepy.errors.TweepyException as e:
            print(f"❌ Twitter API エラー: {e}")
            return []
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
            return []

    def save_tweets(self, tweets, filename='tweets.json'):
        """ツイートをJSONファイルに保存"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)
        print(f"💾 {filename} に保存しました")


def main():
    """メイン処理"""
    print("=" * 60)
    print("ポケモンカード抽選情報 Twitter収集")
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # TwitterFetcherを初期化
    fetcher = TwitterFetcher()

    since_date = datetime.now() - timedelta(days=1)
    all_tweets = []

    # 1. @pokecamatomeru のツイートを取得
    print("\n" + "=" * 60)
    print("📋 1. @pokecamatomeru のツイートを取得")
    print("=" * 60)

    user_tweets = fetcher.fetch_user_tweets(
        username='pokecamatomeru',
        since_date=since_date
    )

    if user_tweets:
        all_tweets.extend(user_tweets)
        fetcher.save_tweets(user_tweets, 'pokecamatomeru_tweets.json')

    # 2. ハッシュタグ検索
    print("\n" + "=" * 60)
    print("📋 2. ハッシュタグで検索")
    print("=" * 60)

    hashtag_tweets = fetcher.search_tweets_by_hashtags(
        since_date=since_date,
        max_results=100
    )

    if hashtag_tweets:
        all_tweets.extend(hashtag_tweets)
        fetcher.save_tweets(hashtag_tweets, 'hashtag_tweets.json')

    # 3. 統合結果を保存
    if all_tweets:
        # 重複を除去（同じIDのツイートを排除）
        unique_tweets = {tweet['id']: tweet for tweet in all_tweets}.values()
        unique_tweets = sorted(unique_tweets, key=lambda x: x['created_at'], reverse=True)

        fetcher.save_tweets(list(unique_tweets), 'all_lottery_tweets.json')

        # 抽選関連ツイートを表示
        print("\n" + "=" * 60)
        print("🎯 抽選関連ツイート（統合結果）")
        print(f"📊 合計 {len(unique_tweets)}件（重複除外後）")
        print("=" * 60)

        lottery_tweets = [t for t in unique_tweets if t.get('is_lottery_related', False)]
        for tweet in lottery_tweets[:10]:  # 最新10件を表示
            print(f"\n📅 {tweet['created_at']}")
            print(f"👤 @{tweet.get('username', 'unknown')}")
            print(f"📝 {tweet['text'][:100]}...")
            print(f"🔗 {tweet['url']}")
            print(f"❤️ {tweet['likes']} 🔄 {tweet['retweets']}")
    else:
        print("\n❌ ツイートを取得できませんでした")


if __name__ == '__main__':
    main()
