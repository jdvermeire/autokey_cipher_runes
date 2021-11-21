import numpy as np
import helper_functions as hpf
import lp_text
import timeit
import multiprocessing as mp


def collect_results(result):
    global best_keys
    best_keys.add(result)


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    start = timeit.default_timer()
    algorithm = 1  # Vigenere, Autokey
    shift_id = 0  # 0 Without #1 +Totient shift, #2 -Totient shift, #3 +prime shift, #4 -prime shift, #5 +index shift, #6 -index shift
    reversed_text = False
    reverse_gematria = False
    interrupter = 0

    ct_numbers = lp_text.get_hollow_text()
    ct_interrupters = np.int8((ct_numbers == interrupter))
    number_of_interrupters = sum(ct_interrupters)

    if reversed_text:
        ct_numbers = ct_numbers[::-1]

    if shift_id > 0:
        ct_numbers = hpf.apply_shift(ct_numbers, shift_id)

    probabilities = hpf.read_data_from_file("new_quadgrams.txt")
    if reverse_gematria:
        probabilities = probabilities[::-1]

    best_keys = hpf.BestKeyStorage()

    for counting in range(pow(2, number_of_interrupters)):
        pool.apply_async(hpf.finding_keys,
                         args=(counting, ct_numbers, ct_interrupters, number_of_interrupters, probabilities, algorithm, reversed_text,
                               reverse_gematria),
                         callback=collect_results)

    pool.close()
    pool.join()

    f = open('keys.txt', 'w')
    for t in best_keys.store:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()

    stop = timeit.default_timer()

    print('Time: ', stop - start)
