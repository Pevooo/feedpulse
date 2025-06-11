import pandas as pd
import pickle
import redis


class RedisManager:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def cache_dataframe(
        self, start_date: str, end_date: str, page_id: str, df: pd.DataFrame
    ):
        self.redis.set(start_date + end_date + page_id, pickle.dumps(df), ex=3600)

    def get_dataframe(
        self, start_date: str, end_date: str, page_id: str
    ) -> pd.DataFrame:
        return pickle.loads(self.redis.get(start_date + end_date + page_id))
