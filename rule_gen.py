import main, rule_book as rb
import numpy as np
import multiprocessing
from functools import partial
#print("Number of cpu : ", multiprocessing.cpu_count())


def rule_generator(i, bit, is_print_rule, is_display, is_save, dim, steps):
    """
    Method finding binary rules for a given decimal number and the intended number of bits
    :param i: a decimal number that can be expressed within the range of the defined bits
    :param bit: defined number of bits
    """
    rule = rb.init_rule[bit]  # Get initial rule from rule book
    # convert decimal to binary
    _binary = bin(i).replace("0b", "").zfill(bit)

    # loop through binary string and add digit to rule dictionary
    for idx, digit in enumerate(_binary):
        key = list(rule.keys())[idx]
        rule[key] = int(digit)
        rule["title"] = f"Rule {str(i)} ({bit} bit)"

    if is_print_rule:
        print(f"rule{i} =", rule)

    if is_display or is_save:
        g = main.Grid(dim=dim, grid_name=rule["title"])
        g.init_grid()
        main.apply_rule(rule=rule, grid=g.get_grid(), steps=steps)
        g.visualize(is_display, is_save)


if __name__ == '__main__':
    #lower_bound = 2000
    #upper_bound = int(2**32 * 0.5)
    #np.random.seed(2024)
    #range = np.random.randint(lower_bound, upper_bound, 6000)
    decimal_number_range = range(0, 4)
    #decimal_number_range = [90]

    max_cpu = multiprocessing.cpu_count()
    cpu = len(decimal_number_range) if len(decimal_number_range) < max_cpu - 2 else max_cpu - 2
    print(f"cpu used: {cpu} from {max_cpu}")
    with multiprocessing.Pool(cpu) as pool:
        pool.map(partial(rule_generator,
                         bit=2,
                         is_print_rule=True,
                         is_display=True,
                         is_save=True,
                         dim=300,
                         steps=300
                         ),
                 decimal_number_range
                 )
