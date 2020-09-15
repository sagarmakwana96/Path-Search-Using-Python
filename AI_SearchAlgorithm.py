import queue
import heapq
import math

def solution (parent, landing_site, parent_child, flag) :
	final_path = [tuple(parent[::-1])]
	if flag == 0 :
		while (parent != tuple(landing_site)):
			parent = parent_child.get(tuple(parent))
			final_path.append(parent[::-1])
	return (final_path[::-1])

def bfs (elevation_grid, n_target, target_site, landing_site, max_elevation) :
	rows = [-1, -1, 0, 1, 1, 1, 0, -1]
	cols = [0, 1, 1, 1, 0, -1, -1, -1]
	
	parent_child = {}
	target_site = target_site[::-1]
	landing_site = landing_site[::-1]
	frontier = queue.Queue()
	frontier.put (landing_site)
	explored_nodes = []
	flag = 0

	if (landing_site == target_site):
		flag =1
		return True, solution(target_site, landing_site, parent_child, flag)	

	while True :
		if (frontier.empty()) :
			return False, ["FAIL"]
		node = frontier.get()
		explored_nodes.append(node)
		for i in range (len(rows)) :
			if (node[0] + rows[i] >= 0 and node[0] + rows[i] < width_height[1] and node[1] + cols[i] >= 0 and node[1] + cols[i] < width_height[0]) : 
				child = [node[0] + rows[i], node[1] + cols[i]]
				child_elevation = abs(elevation_grid[node[0]][node[1]] - elevation_grid[node[0] + rows[i]][node[1] + cols[i]])
				if (child not in explored_nodes and child not in list(frontier.queue) and child_elevation <= max_elevation) :
					if (child == target_site):
						parent_child[tuple(child)] = tuple(node)
						return True, solution(target_site, landing_site, parent_child, flag)
						break
					else :
						parent_child[tuple(child)]=tuple(node)
						frontier.put(child)

def ucs(elevation_grid, n_target, target_site, landing_site, max_elevation) :
	rows = [-1, -1, 0, 1, 1, 1, 0, -1]
	cols = [0, 1, 1, 1, 0, -1, -1, -1]
	traverse_cost = [0]*8
	for i in range (8) :
		if (rows[i] == 0 or cols[i] == 0) :
			traverse_cost[i] = 10
		else :
			traverse_cost[i] = 14

	parent_child = {}
	target_site = target_site[::-1]
	landing_site = landing_site[::-1]
	frontier = []
	heapq.heapify(frontier)
	path_cost = 0
	initial_state = [path_cost, tuple(landing_site)]
	heapq.heappush (frontier, initial_state)
	explored_nodes = []
	flag = 0

	if (landing_site == target_site) :
		flag = 1
		return True, path_cost, solution(target_site, landing_site, parent_child, flag)

	while True :
		if not frontier :
			return False, -1, ["FAIL"]
		node = heapq.heappop(frontier)
		current_node = list(node[1])
		x_cost = node[0]
		if current_node == target_site :
			return True, x_cost, solution(target_site, landing_site, parent_child, flag)
		explored_nodes.append(current_node)
		for i in range (len(rows)) :
			if (current_node[0] + rows[i] >= 0 and current_node[0] + rows[i] < width_height[1] and current_node[1] + cols[i] >= 0 and current_node[1] + cols[i] < width_height[0]) : 
				child = [current_node[0] + rows[i], current_node[1] + cols[i]]
				child_elevation =  abs(elevation_grid[current_node[0]][current_node[1]] - elevation_grid[current_node[0] + rows[i]][current_node[1] + cols[i]])
				y_cost = x_cost + traverse_cost[i]
				if (child not in explored_nodes and child not in [k[1] for k in frontier] and child_elevation <= max_elevation) :
					parent_child[tuple(child)]=tuple(current_node)
					print(child, current_node)
					heapq.heappush(frontier,[y_cost,child])
				elif child in [m[1] for m in frontier] :
					for j in range(len(frontier)):
						if frontier[j][1] == child :
							break

					if y_cost < frontier[j][0] :
						frontier.pop(j)
						heapq.heappush(frontier, [y_cost, child])
						print(child, current_node)
						parent_child[tuple(child)]=tuple(current_node)

def cost_to_target(current_node, target_site) :
	dist = math.pow(math.pow(current_node[0] - target_site[0], 2) + math.pow(current_node[1] - target_site[1], 2), 0.5)
	return dist

def a_star(elevation_grid, n_target, target_site, landing_site, max_elevation) :
	rows = [-1, -1, 0, 1, 1, 1, 0, -1]
	cols = [0, 1, 1, 1, 0, -1, -1, -1]
	traverse_cost = [0]*8
	for i in range (8):
		if rows[i] == 0 or cols[i] == 0 :
			traverse_cost[i] = 10
		else:
			traverse_cost[i] = 14

	parent_child = {}
	target_site = target_site[::-1]
	landing_site = landing_site[::-1]
	frontier = []
	heapq.heapify(frontier)
	path_cost = 0
	distance = cost_to_target(landing_site, target_site)
	initial_state = [distance, path_cost, tuple(landing_site)]
	heapq.heappush (frontier, initial_state)
	explored_nodes = []
	flag = 0

	if (landing_site == target_site) :
		flag = 1
		return True, path_cost, solution(target_site, landing_site, parent_child, flag)

	while True :
		if not frontier :
			return False, -1, ["FAIL"]
		node = heapq.heappop(frontier)
		current_node = list(node[2])
		x_cost = node[1]
		if (current_node == target_site) :
			return True, x_cost, solution(target_site, landing_site, parent_child, flag)
		explored_nodes.append(current_node)
		for i in range (len(rows) ) :
			if (current_node[0] + rows[i] >= 0 and current_node[0] + rows[i] < width_height[1] and current_node[1] + cols[i] >= 0 and current_node[1] + cols[i] < width_height[0]) : 
				child = [current_node[0] + rows[i], current_node[1] + cols[i]]
				child_elevation = abs(elevation_grid[current_node[0]][current_node[1]] - elevation_grid [current_node[0] + rows[i]][current_node[1] + cols[i]])
				y_cost = x_cost + traverse_cost[i] + child_elevation
				distance = cost_to_target(current_node, target_site)
				if (child not in explored_nodes and child not in [k[2] for k in frontier] and child_elevation <= max_elevation ) :
					parent_child[tuple(child)]=tuple(current_node)			
					heapq.heappush(frontier,[y_cost + distance, y_cost,child])
				elif child in [m[1] for m in frontier] :
					for j in range(len(frontier)):
						if frontier[j][1] == child :
							break
					if y_cost < frontier[j][0] :
						frontier.pop(j)
						heapq.heappush(frontier,[y_cost+distance, y_cost, child])
						parent_child[tuple(child)]=tuple(current_node)

if __name__ == "__main__" :
	#reading input file
	input_file = open("input.txt","r+")

	#slecting the algorithm
	search_algo = input_file.readline().split()[0]
	#print(search_algo)

	#storing Width and Height
	width_height = input_file.readline().split()
	width_height = list(map(int, width_height))

	#storing the coordinates of the landing site
	landing_site = input_file.readline().split()
	landing_site = list(map(int, landing_site))

	#storing the maximum elevation permitted
	max_elevation = int(input_file.readline().split()[0])

	#storing the number of target site
	n_target = int(input_file.readline().split()[0])

	#storing the coordinates of the target site
	target_sites = []
	for x in range(n_target) :
		target_sites.append( list(map(int,input_file.readline().split())) )

	elevation_grid = []
	for x in range(width_height[1]) :
		elevation_grid.append(list(map(int, input_file.readline().split())))

	final_path_list = []
	dict_status = {}
	for target_site in target_sites:
		if search_algo == 'BFS' :
			status, final_path = bfs(elevation_grid, n_target, target_site, landing_site, max_elevation)
			final_path_list.append(final_path)
			dict_status[tuple(final_path)] = status
		elif search_algo == 'UCS' :
			status, cost, final_path = ucs(elevation_grid, n_target, target_site, landing_site, max_elevation)
			final_path_list.append(final_path)
			dict_status[tuple(final_path)] = status
			print(cost)
		elif search_algo == 'A*' :
			status, cost, final_path = a_star(elevation_grid, n_target, target_site, landing_site, max_elevation)
			final_path_list.append(final_path)
			dict_status[tuple(final_path)] = status
			print(cost)

	print(final_path_list)
	file = open('output.txt','w')
	for i in final_path_list :
		if dict_status[tuple(i)] == False :
			file.write("FAIL")
			file.write("\n")
		else :
			for j in i :
				file.write(str(j[0]) + "," + str(j[1]) + " ")
			file.write("\n")
	file.close()
