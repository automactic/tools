import requests
import base64
import functools

API_KEY = ''
API_SECRET = ''


class Base:
    @property
    @functools.lru_cache()
    def token(self):
        """Download the bearer token and return it.
        Args:
            key: API key.
            secret: API string.
        """

        # setup
        credential = base64.b64encode(
            bytes(f"{API_KEY}:{API_SECRET}", "utf-8")
        ).decode()
        url = "https://api.twitter.com/oauth2/token"
        headers = {
            "Authorization": f"Basic {credential}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        payload = {"grant_type": "client_credentials"}

        # post the request
        response = requests.post(url, headers=headers, params=payload)

        # check the response
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise

class Archiver(Base):
    def list(self, user, start=None, count=200, rts=False):
        """Download user's tweets and return them as a list.
        Args:
            user: User ID.
            start: Tweet ID.
            rts: Whether to include retweets or not.
        """

        # setup
        bearer_token = self.token
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        headers = {"Authorization": f"Bearer {bearer_token}"}
        payload = {
            "screen_name": user,
            "count": count,
            "include_rts": rts,
            "tweet_mode": "extended",
        }
        if start:
            payload["max_id"] = start

        # get the request
        r = requests.get(url, headers=headers, params=payload)

        # check the response
        if r.status_code == 200:
            tweets = r.json()
            if len(tweets) == 1:
                return []
            else:
                return tweets if not start else tweets[1:]
        else:
            print(
                "An error occurred with the request,"
                + f"the status code was {r.status_code}"
            )
            return []



if __name__ == '__main__':
    archiver = Archiver()
    results = archiver.list('user_name')
    print(results)