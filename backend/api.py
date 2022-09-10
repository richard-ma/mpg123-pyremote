from flask import Flask
from flask_restful import Resource, Api
import player
import os


MUSIC_DIRECTORY = '/home/share/Music'


app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)


def make_response(message=None, err=None):
    return {
        'message': message,
        'error': err,
    }


class Track:
    def __init__(self, track_name):
        self.track_name = track_name

    def full_path_name(self):
        return os.path.join(MUSIC_DIRECTORY, self.track_name)


class Play(Resource):
    # get track info
    def get(self, track_name):
        t = Track(track_name)
        player = app.config['music_player']
        try:
            player.play(t.full_path_name())

            return make_response(t.full_path_name())
        except Exception as e:
            return make_response(err=e)


api.add_resource(Play, '/play/<string:track_name>')

if __name__ == "__main__":
    # Setup code
    music_player = player.Player.factory(player_name='mpg321')
    app.config['music_player'] = music_player

    music_player.run()

    # Running API Server
    app.run('0.0.0.0', debug=True)

    # clean & quit
    music_player.quit()
