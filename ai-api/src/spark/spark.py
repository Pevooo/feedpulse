import enum


class SparkTable(enum):
    REPORTS = "reports"
    INPUT_COMMENTS = "input_comments"
    PROCESSED_COMMENTS = "processed_comments"
    PAGES = "pages"


class Spark:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Spark, cls).__new__(cls)
        return cls.instance

    def add(self, table: enum, row_data: str):
        pass

    def delete(self, table: enum, row_data: str):
        pass

    def query(self, table: enum, row_data: str):
        pass

    def modify(self, table: enum, row_data: str):
        pass


spark_instance = Spark()
