from abc import ABC, abstractmethod
import subprocess


class Player(ABC):
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
    def mute(self, op=True):
        pass

    @abstractmethod
    def volume(self, percent):
        pass


class mpg321_Player(Player):
    def __init__(self):
        self.p = None
        self._volume = 50  # 50% volume

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
        if self.p is not None:
            self.__write(f'LOAD {track_name}'.format(track_name=track_name))
            return True
        else:
            return False

    def pause(self):
        if self.p is not None:
            self.__write('PAUSE')

    def stop(self):
        if self.p is not None:
            self.__write('STOP')

    def mute(self, mute=True):
        if self.p is not None:
            if mute:
                self.volume(0)
            else:
                self.volume(self._volume)

    def volume(self, percent):
        if self.p is not None:
            self._volume = percent
            self.__write(f'GAIN {percent}'.format(percent=percent))


if __name__ == "__main__":
    track_name = '/home/share/Music/周杰伦-听见下雨的声音.mp3'
    player = mpg321_Player()
    player.run()
    player.play(track_name)
