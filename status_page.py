import argparse

import bottle
from bottle_cors_plugin import cors_plugin

from a2s_util import get_server_info

app = bottle.app()
app.install(cors_plugin("*"))


@app.route("/get_info", method="GET")
def get_info():
    try:
        info = get_server_info()
        ret_data = {"numPlayers": info.player_count, "serverUp": True}
    except Exception as e:
        import traceback

        traceback.print_exc()
        ret_data = {"numPlayers": 0, "serverUp": False}
    return ret_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Valheim Status Server")
    parser.add_argument("-s", "--server-type", default="auto", choices=["gunicorn"])
    parser.add_argument("-w", "--workers", type=int, default=1)
    parser.add_argument("-r", "--auto-reload", action="store_true", default=False)
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
    )

    args = parser.parse_args()
    app.run(
        host="localhost",
        port=args.port,
        server=args.server_type,
        workers=args.workers,
        reloader=args.auto_reload,
    )
