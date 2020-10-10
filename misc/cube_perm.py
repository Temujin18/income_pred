from itertools import permutations, count
import itertools
import profile
# import numpy as np
# import pandas as pd
import collections
# from sympy.utilities.iterables import multiset_permutations

import timeit

# def perms(n):
#     """
#     Returns permutations of n that is a perfect cube.
#     Really slow. Don't bother.
#     """
#     n = str(n)
#     int_list = list(map(int,(''.join(x) for x in permutations(n))))
#     result = [num for num in int_list if (round(num**(1/3)))**3 == num]
#     return set(result)  #permutation elements are treated unique based on position, not by values. duplicates possible, therefore set().
    
# def perms_v2(n):
#     """
#     Permutations using numpy and sympy.
#     Still very slooow. Don't bother.
#     """
#     n = list(map(int, list(str(n))))
#     n = np.array(n)
#     permutations = [p for p in multiset_permutations(n)]
#     return permutations

# SOLUTION
# Abandon use of permutations in solution due to O(k*n!) complexity:
# https://stackoverflow.com/questions/25735762/big-o-notation-for-the-permutations-of-a-list-of-words

# Class for incrementing counts of cubes and storing cubed numbers in a list
# Based on https://stackoverflow.com/questions/8483881/defaultdict-and-tuples
class Cubes(object):
    __slots__ = ('count', 'cubes') # slots for memory and access time gains

    def __init__(self):
        self.count = 0
        self.cubes = []
    def __iadd__(self, num):
        self.count += 1
        self.cubes.append(num)
        return self

def cube_perms(num_perms=5):
    """
    Returns smallest cubed number based on num of permutations
    """
    cubed_counts = collections.defaultdict(Cubes)

    result = None
    for i in count(start=1):
        cubed_num = i**3
        perm = ''.join(sorted(str(cubed_num))) # encountered cubed_num sorted into single string

        if result is not None and len(perm) > len(str(result)):
            return result # return result if result exists and shorter than current perm
        
        cubed_counts[perm] += cubed_num # count each 'permutation' and add cubed_num to list of cubes

        if cubed_counts[perm].count == num_perms:
            if not has_more_cubes(perm, i):
                smallest_cube = min(cubed_counts[perm].cubes)
                if result is None or smallest_cube < result:
                    result = smallest_cube

# check if cubed number only has cube roots equal to num_perms
# Based on https://codereview.stackexchange.com/questions/107508/project-euler-62-cubic-permutations-logic
def has_more_cubes(perm, i):
    max_possible = int(int(''.join(perm[::-1]))**(1/3.)) #reverse of perm is highest num suspected to be perfect cube
    return any( ''.join(sorted(str(p**3))) == perm
                for p in range(i+1, max_possible)) # return True if there exists a perfect cube beyond i+1.


profile.run('print(f"ANSWER: {cube_perms()}")')
# t = timeit.Timer('cube_perms()','from cube_perm import cube_perms')
# runs = t.repeat(100,1)
# print(min(runs))
# method runs at around 0.23 s 

