import requests


class ReportHandler:
    def send_report(self, report: str, url: str):
        requests.post(url, json=report)
