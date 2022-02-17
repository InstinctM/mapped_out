from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return

@app.get("/radius/")
def get_videos(xCor : str, yCor: str):
    """ Connects to the database, returns all videos in radius. """
    return {xCor, yCor}

@app.post("/upload/")
def post_videos(userHash: str, video: str):
    """ Connects to the database, stores uploaded video under given Username. """
    pass