import csv

#Function to load coordinates csv file
def coordinates(filename = 'coordinates.csv'):
    coordinates = {}
    try:
        with open(filename, newline = '') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                city = row[0]
                lat = float(row[1])
                lon = float(row[2])
                coordinates[city] = (lat, lon)
    except FileNotFoundError:
        print('File not found')
    return coordinates

# Function to load adjacencies txt file
def adjacencies(filename = 'adjacencies.txt'):
    adjacencies = {}
    try:
        with open(filename, 'r') as txtfile:
            for line in txtfile:
                city1, city2 = line.strip().split()
                if city1 not in adjacencies:
                    adjacencies[city1] = []
                if city2 not in adjacencies:
                    adjacencies[city2] = []
                    adjacencies[city1].append(city2)
                    adjacencies[city2].append(city1)
    except FileNotFoundError:
        print('File not found')
    return adjacencies

coordinates = coordinates()
adjacencies = adjacencies()

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    # method to add edges
    def add_edge(self, city1, city2):
        if city1 not in self.adjacency_list:
            self.adjacency_list[city1] = []
        if city2 not in self.adjacency_list:
            self.adjacency_list[city2] = []
        self.adjacency_list[city1].append(city2)
        self.adjacency_list[city2].append(city1)

    # method to display adjacency list of the map
    def display_graph(self):
        for city, neighbors in self.adjacency_list.items():
            print(f"{city}: {', '.join(neighbors)}")

graph = Graph()
for city, neighbors in adjacencies.items():
    for neighbor in neighbors:
        graph.add_edge(city, neighbor)


print("Graph of cities and their adjacencies:")
graph.display_graph()


# Brute-Force search
def brute_force_search(graph, start, goal, path = []):
    path = path + [start]

    if start == goal:
        return path
    
    if start not in graph.adjacency_list:
        return None
    
    for neighbor in graph.adjacency_list[start]:
        if neighbor not in path:
            new_path = brute_force_search(graph, neighbor, goal, path)
            if new_path:
                return new_path
    
    return None

from collections import deque

# Breadth First Search (BFS)
def bfs(graph, start, goal):
    visited = set()                         # To keep track of visited nodes
    queue = deque([[start]])                # Queue to store paths

    if start == goal:
        return [start]
    
    while queue:
        path = queue.popleft()
        city = path[-1]

        if city not in visited:
            neighbors = graph.adjacency_list[city]
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

                if neighbor == goal:
                    return new_path
                
            visited.add(city)

    return None

print('------------------------------------------------------------------------------------------------------------------')
# Test Brute-Force and BFS
start_city = 'Anthony'
goal_city = 'Wichita'

# Brute-Force Search
print("\nBrute-Force Search Result:")
brute_force_result = brute_force_search(graph, start_city, goal_city)
if brute_force_result:
    print(f"Route found: {brute_force_result}")
else:
    print("No route found.")

# Breadth-First Search
print("\nBreadth-First Search Result:")
bfs_result = bfs(graph, start_city, goal_city)
if bfs_result:
    print(f"Route found: {bfs_result}")
else:
    print("No route found.")
