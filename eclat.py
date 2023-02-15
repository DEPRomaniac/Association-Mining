# SepehrAhmadi-810897031
import pandas as pd
from pyECLAT import ECLAT
import csv

def readmlmovie():
	ratings_file = open('ratings.csv')
	ratings_data = []

	header = next(ratings_file)
	dataset = {}
	for row in ratings_file:
		uid, mid, rating = list(map(float, row.split(',')))
		uid, mid = int(uid), int(mid)
		if rating >= 3:
			if uid not in dataset:
				dataset[uid] = [mid]
			else:
				dataset[uid].append(mid)
	ratings_file.close()
	return list(dataset.values())

transactions = readmlmovie()

data = pd.DataFrame(transactions)
min_n_products = 1
min_support = 100/len(transactions)
max_length = max([len(x) for x in transactions])

my_eclat = ECLAT(data=data, verbose=True)
rule_indices, rule_supports = my_eclat.fit(min_support=min_support, min_combination=min_n_products, max_combination=max_length)
print(rule_supports)