import unittest
import random as rnd


from main import get_win_sequence, get_water_volume


class TestCase(unittest.TestCase):
    def test_get_win_sequence(self):
        test_data = [['4\nMAMA', 'A'],
                     ['4\nALLOALLO', 'ALLO'],
                     ['5\nBBABBABB', 'ABB'],
                     ['6\nABCOAX', 'ABCOAX'],
                     ['6\nABABABABAB', 'AB'],
                     ['21\nASZYAFAXZEWWAVQHJHBPELYZP', 'AFAXZEWWAVQHJHBPE'],
                     ['28\nAAPQJZAPTAKAAZFJROGIMRNBJZAK',
                      'AAPQJZAPTAKAAZFJROGIMRNBJZAK'],
                     ['28\nEAUBIYTDBVLMGPDBQFBOLJRVXVVUUSEI',
                      'AUBIYTDBVLMGPDBQFBOLJRVXVVU']]
        for input_str, win_str in test_data:
            self.assertEqual(win_str, get_win_sequence(input_str))

    def test_get_win_sequence_random(self):
        for _ in range(100):
            input_str = TestCase.__generate_random_data(1200, 1000)
            win_str = get_win_sequence(input_str)
            self.assertTrue(TestCase.__check_win_sequence(input_str, win_str))

    def test_get_water_volume(self):
        test_data = [['1\n1', 0],
                     ['2\n1 2', 0],
                     ['3\n1 2 3', 0],
                     ['3\n3 2 1', 0],
                     ['3\n3 1 3', 2],
                     ['5\n3 1 3 1 5', 4],
                     ['5\n3 1 3 3 3', 2]]
        for input_str, volume in test_data:
            self.assertEqual(volume, get_water_volume(input_str))

    def test_get_water_volume_long_str(self):
        numbers = ['2'] + ['1'] * 99998 + ['2']
        long_str = '100000\n' + ' '.join(numbers)
        self.assertEqual(99998, get_water_volume(long_str))

    @staticmethod
    def __check_win_sequence(input_string: str, win_seq: str) -> bool:
        rows = input_string.splitlines()
        length = int(rows[0])
        sequence = str(rows[1])
        if len(win_seq) > length:
            print('your sequence is longer than the source sequence')
            return False
        for i in range(len(win_seq) - 1, -1, -1):
            offset = length - len(win_seq)
            if sequence[i + offset] != win_seq[i]:
                print('your sequence is not a substring of the source sequence')
                return False
        for i in range(length):
            if win_seq > sequence[i:length]:
                print(f'length = {length}')
                print(f'source sequence [{sequence[0:length]}]')
                print(f'[{sequence[i:length]}] is less than [{win_seq}]')
                return False
        return True

    @staticmethod
    def __generate_random_data(total_limit: int, target_limit: int) -> str:
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        total_len = rnd.randint(1, total_limit)
        target_len = rnd.randint(1, min(target_limit, total_len))
        return (str(target_len) + '\n' +
                ''.join([rnd.choice(chars) for _ in range(total_len)]))


if __name__ == '__main__':
    unittest.main()
