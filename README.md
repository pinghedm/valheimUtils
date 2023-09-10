# valheimUtils

## Usage

- this repo contains
    - a command line tool for querying the server, run `./a2s_util.py` after install requirements for options
    - a bottle server for providing an http interface to the query tool
    - a webpage that queries the bottle server

### To Run Webservice Locally

- you'll need to write a private_data.py file in the repo root.  It should look something like

```
address = (server_address, query_port)
thread_id = discord thread you want to notify (or just '', only applies if testing notification)
webhook_url = discord webhook url (or just '', only applies if testing notification)
ANTHONY_ID = discord user id (or just '', only applies if testing notification)
DANNY_ID = discord user id (or just '', only applies if testing notification)
notify_file_path = "/tmp/valheim_notify_status"  (or whatever file you want, make sure its writeable)
```

- technically this is all you need - you can then run the backend and frontend yourself
    - serve status_page.html however you'd like
    - start the backend with `python status_page.py`  you probably want to add -r, for autoreload, while developing, if working on the server
- you may wish to install Task [https://taskfile.dev/installation/] to make use of the Taskfile in the repo.
- in that case you can run `task up` to run both, or `task backend` or `task frontend` to run either
- the task file also have some deploy tasks that are hard coded to put the files where I want them on my server; if you wanted to deploy this somewhere you're welcome to adapt it using your own task includes
