from abc import ABC, abstractmethod
import subprocess


class Player(ABC):
    @staticmethod
    def factory(player_name):
        d = {
            'mpg321': mpg321_Player,
        }

        if player_name in d.keys():
            return d[player_name]()
        else:
            raise Exception(f'No such player: {player_name}'.format(player_name=player_name))

    @abstractmethod
    def play(self, track_name):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def mute(self, mute=True):
        pass

    @abstractmethod
    def volume(self, percent):
        pass


class mpg321_Player(Player):
    def __init__(self):
        self.p = None
        self._volume = 100  # 0% ~ 100%

    def __write(self, cmd):
        cmd += '\n'

        try:
            self.p.stdin.write(cmd.encode())
            self.p.stdin.flush()
        except Exception as err:
            raise Exception("{0}: {1}".format(type(err).__name__, err))

    def run(self):
        self.p = subprocess.Popen([
            '/usr/bin/mpg321',
            '-R', 'placeholder',
            '-g', str(self._volume),
            '-q',
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        print("Start Player")

    def play(self, track_name):
        print("Play: ", track_name)
        if not os.path.exists(track_name):
            raise Exception('No such Track')

        if self.p is not None:
            self.__write(f'LOAD {track_name}'.format(track_name=track_name))
            return True
        else:
            raise Exception('Player is None')

    def pause(self):
        if self.p is not None:
            self.__write('PAUSE')

    def stop(self):
        if self.p is not None:
            self.__write('STOP')

    def mute(self, mute=True):
        if self.p is not None:
            if mute:
                self.__volume(0)
            else:
                self.__volume(self._volume)

    def __volume(self, percent):
        if self.p is not None:
            self.__write(f'GAIN {percent}'.format(percent=percent))

    def volume(self, percent):
        self._volume = percent
        self.__volume(percent)

    def quit(self):
        if self.p is not None:
            self.__write('QUIT')
        self.p = None


if __name__ == "__main__":
    import os
    from time import sleep

    working_dir = os.getcwd()

    long_track = os.path.join(working_dir, 'data', 'jay_huahai.mp3')
    short_track = os.path.join(working_dir, 'data', 'Front_Center.wav')
    print(long_track)
    print(short_track)

    player = mpg321_Player()
    player.run()

    player.play(long_track)
    sleep(2)
    player.pause()
    sleep(3)
    player.pause()
    for i in range(10+1):
        sleep(1)
        player.volume(100-i*10)
    for i in range(10+1):
        sleep(1)
        player.volume(i * 10)
    sleep(5)
    player.stop()
    player.quit()
