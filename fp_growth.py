#SepehrAhmadi-810897031
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

class Node:
    def __init__(self, mid, count, parentNode):
        self.mid = mid
        self.count = count
        self.parent = parentNode
        self.children = {}
        self.next = None

    def increment(self, freq):
        self.count += freq

class FPGrowth:
	def __init__(self, pattern_list, min_support):
		self.pattern_list = pattern_list
		self.min_support = min_support

	def process_freq_patt(self):
		fp_tree, header_table = self.build_fptree(self.pattern_list)
		freq_movie_list = []
		self.mine_fptree(set(), header_table, freq_movie_list)
		return freq_movie_list

	def init_header_table(self, movie_set_list):
		header_table = {}
		for movie_set in movie_set_list:
			for mov in movie_set:
				if mov not in header_table:
					header_table[mov] = [1, None]
				else:
					header_table[mov][0] += 1

		for mov,val in list(header_table.items()):
			if val[0] < self.min_support:
				del header_table[mov]

		if(len(header_table) == 0):
			return {}
		return header_table

	def build_fptree(self, movie_set_list):
	    header_table = self.init_header_table(movie_set_list)
	    if(len(header_table) == 0):
	        return None, None
	    fpTree = Node('root', 1, None)
	    for movie_set in movie_set_list:
	        movie_set = [mov for mov in movie_set if mov in header_table]
	        movie_set.sort(key=lambda mov: header_table[mov][0], reverse=True)
	        current_node = fpTree
	        for mov in movie_set:
	            current_node = self.update_tree(mov, current_node, header_table)

	    return fpTree, header_table

	def update_tree(self, mov, tree_node, header_table):
	    if mov in tree_node.children:
	        tree_node.children[mov].increment(1)
	    else:
	        new_movie_node = Node(mov, 1, tree_node)
	        tree_node.children[mov] = new_movie_node
	        self.update_header_table(mov, new_movie_node, header_table)

	    return tree_node.children[mov]

	def update_header_table(self, mov, target_node, header_table):
	    if(header_table[mov][1] == None):
	        header_table[mov][1] = target_node
	    else:
	        current_node = header_table[mov][1]
	        while current_node.next != None:
	            current_node = current_node.next
	        current_node.next = target_node


	def mine_fptree(self, prefix, header_table, freq_movie_list):
	    sorted_movie_list = [mov[0] for mov in sorted(list(header_table.items()), key= lambda x: x[1][0])] 
	    for mov in sorted_movie_list:  
	        updated_prefix = prefix.copy()
	        updated_prefix.add(mov)
	        freq_movie_list.append(updated_prefix)
	        cond_patt_base, freq = self.find_prefix_path(mov, header_table) 
	        cond_tree, cond_header_table = self.build_fptree(cond_patt_base) 
	        
	        if cond_header_table != None:
	            self.mine_fptree(updated_prefix, cond_header_table, freq_movie_list)

	def find_prefix_path(self, base_pattern, header_table):
	    cond_patterns = []
	    freq = []
	    tree_node = header_table[base_pattern][1] 
	    while tree_node != None:

	    	#traverse to root
	        node = tree_node
	        prefix_path = []
	        while node.parent != None:
	        	prefix_path.append(node.mid)
	        	node = node.parent

	        #add pattern to check later
	        if len(prefix_path)>1:
	            cond_patterns.append(prefix_path[1:])
	            freq.append(tree_node.count)

	        # Go to next node
	        tree_node = tree_node.next  
	    return cond_patterns, freq


min_support = 100
dataset = readmlmovie()

fp_algo = FPGrowth(dataset, min_support)
print("frequent patterns are : ", fp_algo.process_freq_patt())