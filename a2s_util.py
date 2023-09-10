#! /usr/bin/env python

import sys
import argparse
import json
import datetime

import a2s
import requests
from private_data import address, webhook_url, ANTHONY_ID, DANNY_ID, notify_file_path


def send_discord_message(message):
    res = requests.post(
        webhook_url,
        json={
            "content": message,
            "username": "Valheim Bot",
            "allowed_mentions": {
                "parse": ["users"],
            },
            "avatar_url": "https://cdn.discordapp.com/attachments/691346224426778644/1145410435391176837/PXL_20230827_172829654.jpg",
        },
    )
    return res


def get_server_info(func_name="info", ret_attr=None):
    func = getattr(a2s, func_name)
    ret = func(address)
    if ret_attr:
        return getattr(ret, ret_attr)
    return ret


def time_to_post(notify_after):
    if notify_after is None:
        return False
    num_fails_recorded = 0
    with open(notify_file_path, "r", encoding="utf8") as f:
        for l in f.readlines():
            if l.startswith("POSTED"):
                return False
            if l.startswith("FAILURE"):
                num_fails_recorded += 1

    return num_fails_recorded >= notify_after


def record_connection_failure():
    with open(notify_file_path, "a", encoding="utf8") as f:
        f.writelines([f"FAILURE: {datetime.datetime.now().isoformat()}\n"])


def record_successful_post():
    with open(notify_file_path, "a", encoding="utf8") as f:
        f.writelines([f"POSTED: {datetime.datetime.now().isoformat()}\n"])


def clear_notify_file():
    with open(notify_file_path, "w", encoding="utf8") as f:
        f.writelines([])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Valheim Server Query Util",
    )
    parser.add_argument("-m", "--method", choices=["info", "players"])
    parser.add_argument("-r", "--return_format", choices=["exit_code", "json"])
    parser.add_argument("-n", "--notify-after", type=int)
    args = parser.parse_args()
    try:
        res = get_server_info(args.method or "info")
        clear_notify_file()
        if args.return_format == "exit_code":
            sys.exit(0)
        elif args.return_format == "json":
            print(json.dumps(dict(res)))
    except Exception as e:
        record_connection_failure()
        if time_to_post(args.notify_after):
            res = send_discord_message(
                f"<@{ANTHONY_ID}>: Looks like the server is down!  (Also, <@{DANNY_ID}> pay attention, in case I am malfunctioning)"
            )
            if res.status_code == 204:
                # if the post to discord succeeds, note that so we stop notifying
                # else well see the fail count on the next go round and try again
                record_successful_post()

        sys.exit(1)
