import random
import time
from functools import lru_cache


def range_sum_no_cache(array, L, R):
    sub_array = array[L:R]
    return sum(sub_array)

def update_no_cache(array, index, value):
    array[index] = value
    return array

@lru_cache(maxsize=1000)
def range_sum_with_cache(array, L, R):
    sub_array = array[L:R]
    return sum(sub_array)

def update_with_cache(array, index, value):
    range_sum_with_cache.cache_clear()
    array[index] = value
    return array


if __name__ == "__main__":
    array = []
    repeatable_part = []
    requests = []
    items = ['Range', 'Update']
    for _ in range(100_001):
        array.append(random.randint(1, 100_000))
    for _ in range(101):
        repeatable_part.append(random.randint(1, 100_000))
    for _ in range(50_001):
        requests.append((random.choice(items), random.choice(repeatable_part), random.choice(repeatable_part)))
    index = random.randint(0, len(array) - 1)
    value = random.randint(1, 100_000)
    start = time.time()
    for i in range(50_001):
        if requests[i][0] == 'Range':
            if requests[i][1] < requests[i][2]:
                L = requests[i][1]
                R = requests[i][2]
            else:
                L = requests[i][2]
                R = requests[i][1]
            range_sum_no_cache(tuple(array), L, R)
        else:
            array = update_no_cache(array, index, value)
    end = time.time()
    time_without_LRU = end - start
    start1 = time.time()
    for i in range(50_001):
        if requests[i][0] == 'Range':
            if requests[i][1] < requests[i][2]:
                L = requests[i][1]
                R = requests[i][2]
            else:
                L = requests[i][2]
                R = requests[i][1]
            range_sum_with_cache(tuple(array), L, R)
        else:
            array = update_with_cache(array, index, value)
    end1 = time.time()
    time_with_LRU = end1 - start1
    print(f"Час виконання без кешування:", time_without_LRU)
    print(f"Час виконання з LRU-кешем:" , time_with_LRU)

'''
CONCLUSIONS
It looks like LRU cache is not sutable for this task. Due to we have array at start 
and this type of data storage already has a very quick access to data. And even if
we increase frequency of repetition in "repeatable_part" to 50 or even to 20 it 
doesn't help due to frequent cache cleaning. I've tried different ways like using
partial caching - sum every 1000, 5000, 10000 or 20000 indexes but the result was
the same.   
'''