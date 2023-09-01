import datetime
import requests

FETCH_URL = "https://validator.nymtech.net/api/v1"


def fetch_data(mix_id: int) -> dict:
    result = {}

    headers = {
        "Accept": "application/json"
    }

    history_req = f"{FETCH_URL}/status/mixnode/{mix_id}/history"
    history_resp = requests.get(
        url=history_req,
        headers=headers
    ).json()

    if "message" in history_resp:
        return {}

    earliest_entry = datetime.datetime.strptime(history_resp["history"][0]["date"], "%Y-%m-%d").strftime("%d.%m.%Y")
    total_uptime = 0
    for entry in history_resp["history"]:
        total_uptime += int(entry["uptime"])

    result["mix_id"] = mix_id
    result["identity"] = history_resp["identity"]
    result["wallet"] = history_resp["owner"]
    result["earliest_entry"] = earliest_entry
    result["all_time_uptime"] = round(total_uptime / len(history_resp["history"]), 2)

    avg_uptime_req = f"{FETCH_URL}/status/mixnode/{mix_id}/avg_uptime"
    avg_uptime_resp = requests.get(
        url=avg_uptime_req,
        headers=headers
    ).json()

    if "message" in avg_uptime_resp:
        return {}

    result["recent_uptime"] = round(float(avg_uptime_resp["node_performance"]["most_recent"]) * 100, 2)
    result["last_hour_uptime"] = round(float(avg_uptime_resp["node_performance"]["last_hour"]) * 100, 2)
    result["last_day_uptime"] = round(float(avg_uptime_resp["node_performance"]["last_24h"]) * 100, 2)

    return result
