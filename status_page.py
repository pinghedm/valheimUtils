import bottle
from a2s_util import get_server_info
from bottle_cors_plugin import cors_plugin
import private_data

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


app.run(
    host="localhost",
    port=getattr(private_data, "port_to_run_server_on", 8000),
    server="gunicorn",
    workers=2,
)
