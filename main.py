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
    autokey = False
    reversed_text = False
    use_totient = False
    use_primes = False
    add_shift = False
    reverse_gematria = False

    CT_numbers = lp_text.get_54_text()

    interrupter = 0
    CT_interrupters = np.int8((CT_numbers == interrupter))
    number_of_interrupters = sum(CT_interrupters)
    interrupters = np.zeros((pow(2, number_of_interrupters), len(CT_numbers)), dtype=np.uint8)

    if reversed_text:
        CT_numbers = CT_numbers[::-1]

    if use_totient:
        CT_numbers = hpf.totient_shift(CT_numbers, use_primes, add_shift)

    quadgrams, probabilities = hpf.read_data_from_file("new_quadgrams.txt")

    if reverse_gematria:
        reverse_quadgrams = np.copy(quadgrams)
        for index in range(29):
            reverse_quadgrams[quadgrams == index] = 28 - index

    for index in range(pow(2, number_of_interrupters)):
        my_dude = np.copy(CT_interrupters)
        bit_rep = bin(int(index))[2:].zfill(number_of_interrupters)
        my_dude[my_dude == 1] = np.array(list(bit_rep))
        interrupters[index] = my_dude

    best_keys = hpf.best_key_storage()

    for counting in range(pow(2, number_of_interrupters)):
        pool.apply_async(hpf.finding_keys,
                         args=(counting, interrupters, CT_numbers, probabilities, autokey, reversed_text),
                         callback=collect_results)

    pool.close()
    pool.join()

    f = open('keys.txt', 'w')
    for t in best_keys.store:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()

    stop = timeit.default_timer()

    print('Time: ', stop - start)

# if __name__ == '__main__':
#    profiler = cProfile.Profile()
#    profiler.enable()
#    main()
#    profiler.disable()
#    stats = pstats.Stats(profiler).sort_stats('tottime')
#    stats.print_stats()
