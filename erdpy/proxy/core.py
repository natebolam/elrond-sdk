import requests
import json
import logging

METACHAIN_ID = 4294967295

logger = logging.getLogger("proxy")


class ElrondProxy:
    def __init__(self, url):
        self.url = url

    def get_account_nonce(self, address):
        url = f"{self.url}/address/{address}/nonce"
        response = requests.get(url)
        response.raise_for_status()
        parsed = json.loads(response.text)
        print(parsed["nonce"])

    def get_account_balance(self, address):
        url = f"{self.url}/address/{address}/balance"
        response = requests.get(url)
        response.raise_for_status()
        parsed = json.loads(response.text)
        print(parsed["balance"])

    def get_account(self, address):
        url = f"{self.url}/address/{address}"
        response = requests.get(url)
        response.raise_for_status()
        parsed = json.loads(response.text)
        print(parsed)

    def get_num_shards(self):
        metrics = self._get_status_metrics(METACHAIN_ID)
        metric = metrics["erd_metric_cross_check_block_height"]
        # number of shard will be equals with how many shard have notarized metachain + 1 (metachain shard)
        print(metric.count(":") + 1)

    def get_last_block_nonce(self, shard_id):
        if shard_id == "metachain":
            metrics = self._get_status_metrics(METACHAIN_ID)
        else:
            metrics = self._get_status_metrics(shard_id)

        print(metrics["erd_probable_highest_nonce"])

    def get_gas_price(self):
        metrics = self._get_status_metrics(0)
        print(metrics["erd_min_gas_price"])

    def get_chain_id(self):
        metrics = self._get_status_metrics(0)
        print(metrics["erd_chain_id"])

    def _get_status_metrics(self, shard_id):
        url = f"{self.url}/node/status/{shard_id}"
        response = requests.get(url)
        response.raise_for_status()
        parsed = json.loads(response.content)
        return parsed["message"]["details"]