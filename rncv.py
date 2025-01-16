"""Update reduced/no CV games from SteamGifts.
"""

import datetime
import json
import logging
import os
import time
import zipfile

import requests


def date_from_sever(timestamp: int) -> str:
    """Return `'YYYY-MM-DD'` from a POSIX timestamp."""
    dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)
    return dt.strftime("%Y-%m-%d %Z")


def output_esgst_data(games_data):
    """Save ESGST data to disk."""
    now_ts = datetime.datetime.now(tz=datetime.UTC).timestamp()
    updateded_timestamp = round(now_ts * 1000)  # in JS, timestamps are in ms
    esgst_data = {
        "v": 13,
        "games": games_data,
        "settings": {
            "lastSyncReducedCvGames": updateded_timestamp,
            "lastSyncNoCvGames": updateded_timestamp,
        },
    }

    os.makedirs("dist", exist_ok=True)
    fname = "esgst_data"
    fspecs = {"encoding": "utf-8", "newline": "\n"}
    with open(f"dist/{fname}.json", "w", **fspecs) as f:
        # For archiving purposes
        json.dump(esgst_data, f, indent=2, sort_keys=True)
    fspecs = {"compression": zipfile.ZIP_DEFLATED, "compresslevel": 9}
    with zipfile.ZipFile(f"dist/{fname}.zip", "w", **fspecs) as z:
        esgst_data_str = json.dumps(esgst_data, separators=(",", ":"))
        z.writestr(f"{fname}.min.json", esgst_data_str)


def update_rncv():
    logger = logging.getLogger(__name__)
    logger.info("Initializing...")
    page = 0
    ended = False
    url = "https://www.steamgifts.com/bundle-games/search"
    error_message = (
        "Internal error when fetching data from SteamGifts. "
        "SteamGifts might be down or the data might not exist. "
        "Please try again later."
    )
    games = {"apps": {}, "subs": {}}

    with requests.Session() as session:
        while not ended:
            time.sleep(1)
            page += 1
            logger.info("Updating RCV/NCV games from SG (page %d...)", page)

            params = {"page": page, "format": "json"}
            response = session.get(url, params=params, timeout=90)
            response.raise_for_status()
            response_json = response.json()
            if not response_json["success"]:
                raise requests.HTTPError(error_message)

            results = response_json["results"]
            for result in results:
                id_ = result["app_id"] or result["package_id"]
                if not id_:
                    continue
                type_ = "app" if result["app_id"] else "sub"
                rcv_timestamp = result["reduced_value_timestamp"]
                ncv_timestamp = result["no_value_timestamp"]
                if rcv_timestamp or ncv_timestamp:
                    game = {}
                    if rcv_timestamp:
                        game["reducedCV"] = date_from_sever(rcv_timestamp)
                    if ncv_timestamp:
                        game["noCV"] = date_from_sever(ncv_timestamp)
                    games[type_ + "s"][str(id_)] = game

            per_page = response_json["per_page"]
            ended = len(results) < per_page

    logger.info("Finalizing...")
    output_esgst_data(games)
    logger.info("Done!")


def main():
    logging.basicConfig(level=logging.INFO)
    update_rncv()


if __name__ == "__main__":
    main()
