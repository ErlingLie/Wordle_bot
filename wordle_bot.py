from multiprocessing.dummy import freeze_support
import numpy as np
from multiprocessing import Pool
from functools import partial
from collections import Counter
def find_pattern(a,b):
    pattern = ["-","-","-","-","-"]
    letters = [c for c in b]
    for i, (l,r) in enumerate(zip(a,b)):
        if l==r:
            pattern[i] = "g"
            letters.remove(l)
    for i, l in enumerate(a):
        if pattern[i] != "g" and l in letters:
            pattern[i] = "y"
            letters.remove(l)
    return "".join(pattern)


def find_probs(guess, true_words):
    pattern_probs = Counter([find_pattern(guess, word) for word in true_words])
    probs = np.array(list(pattern_probs.values()))/len(true_words)
    return probs

def calculate_entropy(probs):
    return -np.dot(probs, np.log2(probs))

def find_entropy(guess,true_words):
    return calculate_entropy(find_probs(guess, true_words))

def reduce_list(guess,true_words,code):
    return [word for word in true_words if find_pattern(guess,word)==code]

if __name__ == "__main__":
    freeze_support()
    with open("true_words.txt") as f:
        true_words = [word.strip() for word in f.readlines()]

    with open("valid_words.txt") as f:
        possible_words = [word.strip() for word in f.readlines()]

    # true_words = reduce_list("crane", true_words, "-----")    
    for i in range(6):
        with Pool(4) as pool:
            entropy = np.array(pool.map(partial(find_entropy, true_words=true_words), possible_words))
        top_indexes = np.argpartition(entropy,-10)[-10:]
        top_entropies = entropy[top_indexes]
        top_words = [possible_words[i] for i in top_indexes]
        top_entropies, top_words  = zip(*sorted(zip(top_entropies, top_words),reverse=True))
        print(top_words)
        print(top_entropies)
        guess = input("Chosen guess: ")
        code = input("Code: ")
        true_words = reduce_list(guess, true_words, code)
        print(f"Now there are {len(true_words)} possible words left")
        if len(true_words) < 10:
            print("They are: ", true_words)