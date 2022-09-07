from random import randint


class Playlist:
    def __init__(self):
        self._q = list()
        self._prev_track_name = None
        self._current_track_name = None
        self._next_func_dict = {
            'sequence': self.__next_func_sequence,
            'random': self.__next_func_random,
            'repeat': self.__next_func_repeat,
        }
        self._next_func_mode = list(self._next_func_dict.keys())[0]
        self._next_func = self._next_func_dict[self._next_func_mode]

    @property
    def length(self):
        return len(self._q)

    @property
    def next_func_mode(self):
        return self._next_func_mode

    def __next_func_sequence(self):
        return self._q.pop(0)

    def __next_func_random(self):
        idx = randint(0, self.length-1)
        return self._q.pop(idx)

    def __next_func_repeat(self):
        if self._current_track_name != self._q[0]:
            self._q.insert(0, self._current_track_name)
        return self._q[0]

    def next_track(self):
        if self.length > 0:
            self._prev_track_name = self._current_track_name
            self._current_track_name = self._next_func()
            return self._current_track_name
        else:
            return None

    def prev_track(self):
        if self._prev_track_name is not None:
            self._current_track_name = self._prev_track_name
            return self._current_track_name
        else:
            return None

    def set_next_func(self, mode):
        if mode in self._next_func_dict.keys():
            self._next_func_mode = mode
            self._next_func = self._next_func_dict[mode]
        else:
            raise Exception("modes: {modes}".format(modes=list(self._next_func_dict.keys())))

    def append(self, track_name):
        self._q.append(track_name)


if __name__ == "__main__":
    def fill(pl):
        for prefix in ['Front', 'Middle', 'Rear']:
            for suffix in ['Top', 'Center', 'Bottom']:
                pl.append('{0}_{1}.wav'.format(prefix, suffix))

    pl = Playlist()
    print("*" * 50)
    print('default: {0}'.format(pl.next_func_mode))
    fill(pl)
    for times in range(pl.length):
        print(pl.next_track())

    print("*" * 50)
    pl.set_next_func('sequence')
    print(pl.next_func_mode)
    fill(pl)
    for times in range(pl.length):
        print(pl.next_track())

    print("*" * 50)
    pl.set_next_func('random')
    print(pl.next_func_mode)
    fill(pl)
    for times in range(pl.length):
        print(pl.next_track())

    print("*" * 50)
    pl.set_next_func('repeat')
    print(pl.next_func_mode)
    fill(pl)
    for times in range(pl.length):
        print(pl.next_track())
