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


def decryption_autokey(key, ct_numbers, current_interrupter):
    mt = np.copy(ct_numbers)
    counter = 0
    index = 0
    while counter < len(key):
        if current_interrupter[index] == 1:
            index += 1
            continue
        else:
            mt[index] = (mt[index] - key[counter]) % 29
            index += 1
            counter += 1

    position = 0

    for i in range(index, len(ct_numbers)):
        if current_interrupter[i] == 1:
            continue
        else:
            mt[i] = (ct_numbers[i] - mt[position]) % 29
            position += 1

    return mt


def decryption_vigenere(key, ct_numbers, current_interrupter):
    mt = np.copy(ct_numbers)
    length_key = len(key)
    counter = 0
    for index in range(len(ct_numbers)):
        if current_interrupter[index]:
            continue
        else:
            mt[index] = (ct_numbers[index] - key[counter % length_key]) % 29
            counter += 1
    return mt


def decryption_autokey_ciphertext(childkey, ct_numbers):
    key_text = np.concatenate((childkey, ct_numbers[0:(len(ct_numbers) - len(childkey))]))
    return np.subtract(ct_numbers, key_text) % 29


def calculate_fitness(childkey, ct_numbers, probabilities, algorithm, current_interrupter, reversed_text):
    mt = None
    if algorithm == 0:
        mt = decryption_vigenere(childkey, ct_numbers, current_interrupter)
    if algorithm == 1:
        mt = decryption_autokey(childkey, ct_numbers, current_interrupter)
    if algorithm == 2:
        mt = decryption_autokey_ciphertext(childkey, ct_numbers)
    if mt is None:
        raise AssertionError()
    if reversed_text:
        mt = mt[::-1]
    indices = np.zeros(((len(mt) - 3),), dtype=int)
    for k in range(len(mt) - 3):
        indices[k] = mt[k] * (29 ** 3) + mt[k + 1] * (29 ** 2) + mt[k + 2] * 29 + mt[k + 3]

    return np.sum(probabilities[indices])


def translate_to_english(parent_key, reverse_gematria):
    dic = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S", "T", "B", "E", "M", "L",
           "ING", "OE", "D", "A", "AE", "Y", "IA", "EA"]
    if reverse_gematria:
        dic.reverse()
    translation = ""
    for index in parent_key:
        translation += dic[index]
    return translation


def translate_best_text(algorithm, best_key_ever, ct_numbers, current_interrupter, reverse_gematria):
    if algorithm == 0:
        return translate_to_english(decryption_vigenere(best_key_ever, ct_numbers, current_interrupter), reverse_gematria)
    if algorithm == 1:
        return translate_to_english(decryption_autokey(best_key_ever, ct_numbers, current_interrupter), reverse_gematria)
    if algorithm == 2:
        return translate_to_english(decryption_autokey_ciphertext(best_key_ever, ct_numbers), reverse_gematria)
    else:
        print('Invlaid algorithm ID')


def finding_keys(counting, interrupters, ct_numbers, probabilities, autokey_id, reversed_text, reverse_gematria):
    current_interrupter = interrupters[counting]
    best_score_ever = -100000.0
    best_key_ever = []
    for key_length in range(1, 16):
        parent_key = np.random.randint(28, size=key_length)
        parent_key[0] = 0
        parent_score = calculate_fitness(parent_key, ct_numbers, probabilities, autokey_id,
                                         current_interrupter, reversed_text)

        still_improving = True

        while still_improving:
            for index in range(len(parent_key)):
                childkey = np.zeros((29, len(parent_key)), dtype=int)

                for jj in range(0, 29):
                    childkey[jj, :] = parent_key

                scores = np.zeros(29)

                for jj in range(0, 29):
                    childkey[jj, index] = jj

                for k in range(0, 29):
                    scores[k] = calculate_fitness(childkey[k, :], ct_numbers, probabilities,
                                                  autokey_id, current_interrupter, reversed_text)

                best_children_score = np.max(scores)

                if best_children_score > parent_score:
                    k = np.where(scores == best_children_score)
                    parent_key = childkey[k[0][0], :]
                    parent_score = best_children_score

            if parent_score > best_score_ever:
                best_score_ever = parent_score
                best_key_ever = parent_key
            else:
                still_improving = False
    print(counting)
    return (best_score_ever, len(best_key_ever),
            translate_best_text(autokey_id, best_key_ever, ct_numbers, current_interrupter, reverse_gematria), best_key_ever,
            translate_to_english(best_key_ever, reverse_gematria))
