import numpy as np
from sympy.ntheory.factor_ import totient
from sympy import prime


def apply_shift(ct_numbers, shift_id):
    if shift_id == 1:
        for index in range(len(ct_numbers)):
            ct_numbers[index] += totient(prime(index + 1))
    if shift_id == 2:
        for index in range(len(ct_numbers)):
            ct_numbers[index] -= totient(prime(index + 1))
    if shift_id == 3:
        for index in range(len(ct_numbers)):
            ct_numbers[index] += prime(index + 1)
    if shift_id == 4:
        for index in range(len(ct_numbers)):
            ct_numbers[index] -= prime(index + 1)
    if shift_id == 5:
        for index in range(len(ct_numbers)):
            ct_numbers[index] += index
    if shift_id == 6:
        for index in range(len(ct_numbers)):
            ct_numbers[index] -= index
    return np.remainder(ct_numbers, 29)


class BestKeyStorage:
    def __init__(self):
        self.store = []
        self.N = 1000

    def add(self, item):
        self.store.append(item)
        self.store.sort(key=lambda x: x[0], reverse=True)
        self.store = self.store[:self.N]


def read_data_from_file(file_name):
    s = open(file_name, "r")
    lines = s.readlines()

    # ints = np.asarray(([line.split(',')[0:4] for line in lines]), dtype=int, order='C')
    probabilities = [line.split(',')[4] for line in lines]
    for index in range(len(probabilities)):
        probabilities[index] = float(probabilities[index].replace('\n', ''))
    probabilities = np.array(probabilities)
    s.close()
    return probabilities


def decryption_autokey(keys, ct_numbers, current_interrupter):
    counter = 0
    index = 0
    key_shape = keys.shape
    key_length = key_shape[1]
    mt = np.repeat(ct_numbers[None], key_shape[0], axis=0)

    if np.sum(current_interrupter[0:key_length]) == 0:
        mt[:, 0:key_length] = (mt[:, 0:key_length] + keys) % 29
        index = key_length
    else:
        while counter < keys.shape[1]:
            if current_interrupter[index] == 1:
                index += 1
                continue
            mt[:, index] = (mt[:, index] + keys[:, counter]) % 29
            index += 1
            counter += 1

    position = 0
    for i in range(index, len(ct_numbers)):
        if current_interrupter[i] == 1:
            continue
        mt[:, i] = (mt[:, i] + mt[:, position]) % 29
        position += 1

    return mt


def decryption_vigenere(keys, ct_numbers, current_interrupter):
    counter = 0
    key_shape = keys.shape
    key_length = key_shape[1]
    mt = np.repeat(ct_numbers[None], key_shape[0], axis=0)

    for index in range(len(ct_numbers)):
        if current_interrupter[index]:
            continue
        else:
            mt[:, index] = (mt[:, index] - keys[:, counter % key_length]) % 29
            counter += 1
    return mt


def calculate_fitness(childkey, ct_numbers, probabilities, algorithm, current_interrupter, reversed_text):
    mt = None
    if algorithm == 0:
        mt = decryption_vigenere(childkey, ct_numbers, current_interrupter)
    if algorithm == 1:
        mt = decryption_autokey(childkey, ct_numbers, current_interrupter)
    if mt is None:
        raise AssertionError()

    if reversed_text:
        mt = mt[::-1]

    len_ciphertext = mt.shape[1]
    indices = np.array(
        [mt[:, 0:len_ciphertext - 3] * 24389, mt[:, 1:len_ciphertext - 2] * 841, mt[:, 2:len_ciphertext - 1] * 29, mt[:, 3:len_ciphertext]])
    score = np.sum(probabilities[np.sum(indices, axis=0)], axis=1)
    return score


def translate_to_english(parent_key, reverse_gematria):
    dic = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S", "T", "B", "E", "M", "L",
           "ING", "OE", "D", "A", "AE", "Y", "IA", "EA"]
    if reverse_gematria:
        dic.reverse()
    translation = ""
    for index in np.nditer(parent_key):
        translation += dic[index]
    return translation


def translate_best_text(algorithm, best_key_ever, ct_numbers, current_interrupter, reverse_gematria):
    if algorithm == 0:
        return translate_to_english(decryption_vigenere(best_key_ever, ct_numbers, current_interrupter), reverse_gematria)
    if algorithm == 1:
        return translate_to_english(decryption_autokey(best_key_ever, ct_numbers, current_interrupter), reverse_gematria)
    else:
        print('Invlaid algorithm ID')


def finding_keys(counting, ct_numbers, ct_interrupters, number_of_interrupters, probabilities, algorithm, reversed_text, reverse_gematria):
    current_interrupter = np.copy(ct_interrupters)
    bit_rep = bin(int(counting))[2:].zfill(number_of_interrupters)
    current_interrupter[ct_interrupters == 1] = np.array(list(bit_rep))
    best_score_ever = -1000000.0
    best_key_ever = []
    for key_length in range(1, 20):
        parent_key = np.random.randint(28, size=(1, key_length))  # np.array([[0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]])
        parent_score = calculate_fitness(parent_key, ct_numbers, probabilities, algorithm, current_interrupter, reversed_text)

        still_improving = True

        while still_improving:
            for index in range(key_length):
                childkey = np.zeros((29, key_length), dtype=int)
                childkey[:] = parent_key

                childkey[:, index] = np.arange(29)
                scores = calculate_fitness(childkey, ct_numbers, probabilities, algorithm, current_interrupter, reversed_text)

                best_children_score = np.max(scores)

                if best_children_score > parent_score:
                    k = np.where(scores == best_children_score)
                    parent_key = childkey[k[0], :]
                    parent_score = best_children_score

            if parent_score > best_score_ever:
                best_score_ever = parent_score
                best_key_ever = parent_key
            else:
                still_improving = False
    print(counting)
    return (best_score_ever, len(best_key_ever),
            translate_best_text(algorithm, best_key_ever, ct_numbers, current_interrupter, reverse_gematria), best_key_ever,
            translate_to_english(best_key_ever, reverse_gematria))
