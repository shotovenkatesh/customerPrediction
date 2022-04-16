from collections import Counter
from functools import reduce
import numpy as np
import pandas as pd



a = ["a","b","c","a","a","b"]

counter = a[0]
solution = []

lettersIndexes = [i for i in range(len(a)) if a[i] == "a" ]
# print(lettersIndexes)
#
# for letter in a:
#     if counter == letter:
#         solution.append(letter)
#
# print(solution)
#
#
#
# # answer = reduce(lambda a, b: a + [b[0]] * b[1], sorted(Counter(a).items(), key=lambda x: x[1], reverse=True), [])
# # print(answer)
#
#
#
#
#
#

tweets = ["rock", "apples", "biscuit", "cycle", "mobile", "machines", "laptop"]

names = ["a", "b", "a", "c", "a", "c", "a"]
answer_dict = {}

#get duplicates,loop and find their index

duplicates = []

for i in names:
    if names.count(i) > 1 and i not in duplicates:
        duplicates.append(i)


print(duplicates)
for dup in duplicates:

    answer_dict[dup] = []
    lettersIndexes = [i for i in range(len(names)) if names[i] == dup]

    for indx in lettersIndexes:
        answer_dict[dup].append(tweets[indx])

print(answer_dict)

