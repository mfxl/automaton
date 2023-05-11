import main, rule_book
import numpy as np
import multiprocessing
#print("Number of cpu : ", multiprocessing.cpu_count())

def rule_generator(i, bit=5):
    current_rule = rule_book.init_rule_3bits if bit == 3 else rule_book.init_rule_5bits
    # convert decimal to 8-digit binary
    _binary = bin(i).replace("0b", "").zfill(2**bit)

    # loop through binary string and add digit to rule dictionary
    for idx, digit in enumerate(_binary):
        key = list(current_rule.keys())[idx]
        current_rule[key] = int(digit)
        current_rule["title"] = f"Rule {str(i)} ({bit} bit)"

    #print(f"rule{i} =", current_rule)

    g = main.Grid(dim=200, grid_name=current_rule["title"])
    g.init_grid()
    main.apply_rule(rule=current_rule, grid=g.get_grid(), steps=200)
    density = g.density
    std = g.std_col
    #print(f"{current_rule['title']} (d, s)", density, std)
    g.visualize()


if __name__ == '__main__':
    lower_bound = 2000
    upper_bound = int(2**32 * 0.5)
    np.random.seed(2024)
    range = np.random.randint(lower_bound, upper_bound, 6000)
    #range = range(0, 256)
    #range = [90]
    with multiprocessing.Pool(16) as p:
        p.map(rule_generator, range)


