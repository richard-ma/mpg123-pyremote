import os
from fastapi import FastAPI
from pydantic import BaseModel
from player import Player


MUSIC_DIRECTORY = '/home/share/Music'
player = Player.factory('mpg321')
app = FastAPI()


class Track(BaseModel):
    track_name: str

    @property
    def filename(self):
        return os.path.join(MUSIC_DIRECTORY, self.track_name + '.mp3')


@app.get('/api/v2/songs')
async def list_songs():
    pass


@app.get('/api/v2/control/play/{song_name}')
async def play(song_name: str):
    track = Track(song_name)

    player.play(track.filename)


@app.get('/api/v2/control/pause')
async def pause():
    player.pause()


@app.get('/api/v2/control/volume/{value}')
async def volume(value: int):
    if value > 100:
        value = 100
    if value < 0:
        value = 0

    player.volume(value)
