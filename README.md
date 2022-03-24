# Mapped Out
### Development Server
#### On Linux:
Install the required modules:

    pip install -r requirements.txt
    # or pip3

Run `run-dev.sh`:
    
    ./run-dev.sh

The web server will be running at `http://localhost:8080` and the api server will be at `http://localhost:8000`

### Trouble Shooting
#### `./run-dev.sh` Permission denied

    sudo chmod u+x run-dev.sh
    ./run-dev.sh

#### `flask` or `uvicorn` command not found

    export PATH=$PATH:~/.local/bin

If it still doesn't work

    alias flask=~/.local/bin/flask
    alias uvicorn=~/.local/bin/uvicorn
