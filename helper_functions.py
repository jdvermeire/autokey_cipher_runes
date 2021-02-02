import numpy as np
from sympy.ntheory.factor_ import totient


def totient_shift(CT_numbers, use_primes, add_shift):
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                       37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                       79, 83, 89, 97, 101, 103, 107, 109, 113,
                       127, 131, 137, 139, 149, 151, 157, 163,
                       167, 173, 179, 181, 191, 193, 197, 199,
                       211, 223, 227, 229, 233, 239, 241, 251,
                       257, 263, 269, 271, 277, 281, 283, 293,
                       307, 311, 313, 317, 331, 337, 347, 349, 353,
                       359, 367, 373, 379, 383, 389, 397, 401, 409,
                       419, 421, 431, 433, 439, 443, 449, 457, 461,
                       463, 467, 479, 487, 491, 499, 503, 509, 521,
                       523, 541, 547, 557, 563, 569, 571, 577, 587,
                       593, 599, 601, 607, 613, 617, 619, 631, 641,
                       643, 647, 653, 659, 661, 673, 677, 683, 691,
                       701, 709, 719, 727, 733, 739, 743, 751, 757,
                       761, 769, 773, 787, 797, 809, 811, 821, 823,
                       827, 829, 839, 853, 857, 859, 863, 877, 881,
                       883, 887, 907, 911, 919, 929, 937, 941, 947,
                       953, 967, 971, 977, 983, 991, 997, 1009, 1013,
                       1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
                       1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123,
                       1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
                       1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277,
                       1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319,
                       1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423,
                       1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471,
                       1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531,
                       1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
                       1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657,
                       1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723,
                       1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789,
                       1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
                       1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949,
                       1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011,
                       2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083,
                       2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141,
                       2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237,
                       2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293,
                       2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357,
                       2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417,
                       2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503,
                       2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591,
                       2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663,
                       2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711,
                       2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777,
                       2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843,
                       2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917,
                       2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001,
                       3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079,
                       3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169,
                       3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251,
                       3253, 3257, 3259, 3271, 3299, 3301])
    if add_shift and use_primes:
        for index in range(len(CT_numbers)):
            CT_numbers[index] += totient(primes[index])
    if not(add_shift) and use_primes:
        for index in range(len(CT_numbers)):
            CT_numbers[index] -= totient(primes[index])
    if add_shift and not use_primes:
        for index in range(len(CT_numbers)):
            CT_numbers[index] += index
    if not add_shift and not use_primes:
        for index in range(len(CT_numbers)):
            CT_numbers[index] -= index
    return np.remainder(CT_numbers, 29)


class best_key_storage:
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

    ints = np.asarray(([line.split(',')[0:4] for line in lines]), dtype=int, order='C')
    probabilities = [line.split(',')[4] for line in lines]
    for index in range(len(probabilities)):
        probabilities[index] = float(probabilities[index].replace('\n', ''))
    probabilities=np.array(probabilities)
    s.close()
    return ints, probabilities


def decryption_autokey(key, CT_numbers, current_interrupter):
    MT = np.copy(CT_numbers)
    counter = 0
    index = 0
    while counter < len(key):
        if current_interrupter[index] == 1:
            index += 1
            continue
        else:
            MT[index] = (MT[index] - key[counter]) % 29
            index += 1
            counter += 1

    position = 0

    for i in range(index, len(CT_numbers)):
        if current_interrupter[i] == 1:
            continue
        else:
            MT[i] = (CT_numbers[i] - MT[position]) % 29
            position += 1

    return MT


def decryption_vigenere(key, CT_numbers, current_interrupter):
    MT = np.copy(CT_numbers)
    length_key = len(key)
    counter = 0
    for index in range(len(CT_numbers)):
        if current_interrupter[index]:
            continue
        else:
            MT[index] = (CT_numbers[index] - key[counter % length_key]) % 29
            counter += 1
    return MT


def calculate_fitness(childkey, CT_numbers, probabilities, autokey, current_interrupter, reversed_text):
    if autokey:
        MT = decryption_autokey(childkey, CT_numbers, current_interrupter)
    else:
        MT = decryption_vigenere(childkey, CT_numbers, current_interrupter)

    if reversed_text:
        MT = MT[::-1]

    indices = np.zeros(((len(MT) - 3),), dtype=int)
    for k in range(len(MT) - 3):
        indices[k] = MT[k] * (29 ** 3) + MT[k + 1] * (29 ** 2) + MT[k + 2] * 29 + MT[k + 3]

    return np.sum(probabilities[indices])


def translate_to_english(parent_key):
    dic = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S", "T", "B", "E", "M", "L",
           "ING", "OE", "D", "A", "AE", "Y", "IA", "EA"]
    translation = ""
    for index in parent_key:
        translation += dic[index]
    return translation
