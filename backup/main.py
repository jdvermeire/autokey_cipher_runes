import numpy as np
import helper_functions as hpf
import lp_text
# import cProfile, pstats
import timeit


def main():
    start = timeit.default_timer()
    autokey = True
    reversed_text = False
    use_totient = False
    use_primes = False
    add_shift = False
    reverse_gematria = False

    CT_numbers = lp_text.get_spiral_branch_text()

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
        current_interrupter = interrupters[counting]
        for key_length in range(6, 25):
            parent_key = np.random.randint(28, size=key_length)
            parent_score = hpf.calculate_fitness(parent_key, CT_numbers, probabilities, autokey,
                                                 current_interrupter, reversed_text)
            best_score_ever = parent_score
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
                        scores[k] = hpf.calculate_fitness(childkey[k, :], CT_numbers, probabilities,
                                                          autokey, current_interrupter, reversed_text)

                    best_children_score = np.max(scores)

                    if best_children_score > parent_score:
                        k = np.where(scores == best_children_score)
                        parent_key = childkey[k[0][0], :]
                        parent_score = best_children_score

                if parent_score > best_score_ever:
                    best_score_ever = parent_score
                    Translation = hpf.translate_to_english(
                        hpf.decryption_autokey(parent_key, CT_numbers, current_interrupter))
                    best_keys.add((best_score_ever, parent_key, Translation))
                else:
                    still_improving = False

        print(counting)

    f = open('keys.txt', 'w')
    for t in best_keys.store:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()

    stop = timeit.default_timer()

    print('Time: ', stop - start)


main()
# if __name__ == '__main__':
#    profiler = cProfile.Profile()
#    profiler.enable()
#    main()
#    profiler.disable()
#    stats = pstats.Stats(profiler).sort_stats('tottime')
#    stats.print_stats()
