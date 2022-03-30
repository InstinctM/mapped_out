# Mapped Out
### Development Server
Install the required modules:

    pip install -r requirements.txt
    # or pip3

#### On Mac/Linux:
Run `run-dev.sh`:
    
    ./run-dev.sh

#### On Windows:

    run-dev.bat

The server will be running at `http://localhost:8000`

### Trouble Shooting
#### `./run-dev.sh` Permission denied

    sudo chmod u+x run-dev.sh
    ./run-dev.sh

#### `flask` or `uvicorn` command not found

    export PATH=$PATH:~/.local/bin

If it still doesn't work

    alias flask=~/.local/bin/flask
    alias uvicorn=~/.local/bin/uvicorn
