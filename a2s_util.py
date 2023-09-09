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


def write_notify_file(data):
    with open(notify_file_path, "w", encoding="utf8") as f:
        f.writelines(data)


def notify_file_has_data():
    with open(notify_file_path, "r", encoding="utf8") as f:
        return bool(f.readlines())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Valheim Server Query Util",
    )
    parser.add_argument("-m", "--method", choices=["info", "players"])
    parser.add_argument("-r", "--return_format", choices=["exit_code", "json"])
    parser.add_argument("-n", "--notify", action="store_true")
    args = parser.parse_args()
    notify_file_name = args.notify_file
    try:
        res = get_server_info(args.method or "info")
        write_notify_file([])
        if args.return_format == "exit_code":
            sys.exit(0)
        elif args.return_format == "json":
            print(json.dumps(dict(res)))
    except Exception as e:
        already_notified = notify_file_has_data()
        if not args.notify and not already_notified:
            res = send_discord_message(
                f"<@{ANTHONY_ID}>: Looks like the server is down!  (Also, <@{DANNY_ID}> pay attention, in case I am malfunctioning)"
            )
            if res.status_code == 204:
                # if the discord message succeeds, note that in a file so we don't ping constantly
                write_notify_file([datetime.datetime.now().isoformat()])
            else:
                # if it fails, hope it succeeds next time I guess?  should have some fallback thing but eh
                write_notify_file([])

        sys.exit(1)
