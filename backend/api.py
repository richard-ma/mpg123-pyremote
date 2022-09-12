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
        self._track_name = track_name

    # for message
    def get_track_name(self):
        return self._track_name

    # for player
    def get_full_path_track_name(self):
        return os.path.join(MUSIC_DIRECTORY, self._track_name + '.mp3')


class Play(Resource):
    # get track info
    def get(self, track_name):
        t = Track(track_name)
        p = app.config['music_player']

        try:
            p.play(t.get_full_path_track_name())

            return make_response(track_name)
        except Exception as e:
            return make_response(err=e)


class Stop(Resource):
    def get(self):
        p = app.config['music_player']

        try:
            p.stop()

            return make_response(True)
        except Exception as e:
            return make_response(err=e)


class Pause(Resource):
    def get(self):
        p = app.config['music_player']

        try:
            p.pause()

            return make_response(True)
        except Exception as e:
            return make_response(err=e)


class Volume(Resource):
    def get(self, percent):
        p = app.config['music_player']

        try:
            p.volume(percent)

            return make_response(percent)
        except Exception as e:
            return make_response(err=e)


api.add_resource(Play, '/play/<string:track_name>')
api.add_resource(Stop, '/stop')
api.add_resource(Pause, '/pause')
api.add_resource(Volume, '/volume/<int:percent>')

if __name__ == "__main__":
    # Setup code
    music_player = player.Player.factory(player_name='mpg321')
    app.config['music_player'] = music_player

    music_player.run()

    # Running API Server
    app.run('0.0.0.0', debug=True)

    # clean & quit
    music_player.quit()
