import csv
import math
import heapq

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

#--------------------------------------------------------------------------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Search Algorithms

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

# Depth First Search 
def dfs_search(graph, start, goal, path =None, visited = None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()

    visited.add(start)

    if start == goal:
        return path
    
    for neighbor in graph.adjacency_list.get(start, []):
        if neighbor not in visited:
            new_path = path + [neighbor]
            result = dfs_search(graph, neighbor, goal, new_path, visited)
            if result:
                return result
            
    return None

# Iterative Deepening DFS
def iddfs_search(graph, start, goal, max_depth=1000):
    def dls(current, goal, depth, path):
        if depth == 0 and current == goal:
            return path
        if depth > 0:
            for neighbor in graph.adjacency_list.get(current, []):
                if neighbor not in path:
                    result = dls(neighbor, goal, depth - 1, path + [neighbor])
                    if result:
                        return result
        return None

    for depth in range(max_depth):
        result = dls(start, goal, depth, [start])
        if result:
            return result
    return None

def best_first_search(graph, start, goal, coordinates):
    open_list = []
    heapq.heappush(open_list, (0, [start]))  # (heuristic value, path)
    visited = set()

    while open_list:
        _, path = heapq.heappop(open_list)
        current = path[-1]

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)
            for neighbor in graph.adjacency_list.get(current, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    priority = heuristic(neighbor, goal, coordinates)
                    heapq.heappush(open_list, (priority, new_path))

    return None

def a_star_search(graph, start, goal, coordinates):
    open_list = []
    heapq.heappush(open_list, (0, [start], 0))  # (f(n), path, g(n))
    visited = set()

    while open_list:
        _, path, g = heapq.heappop(open_list)
        current = path[-1]

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)
            for neighbor in graph.adjacency_list.get(current, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    g_new = g + heuristic(current, neighbor, coordinates)  # g(n)
                    f = g_new + heuristic(neighbor, goal, coordinates)  # f(n) = g(n) + h(n)
                    heapq.heappush(open_list, (f, new_path, g_new))

    return None

# Heuristic Function
def heuristic(city1, city2, coordinates):
    lat1, lon1 = coordinates[city1]
    lat2, lon2 = coordinates[city2]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

print('------------------------------------------------------------------------------------------------------------------')
def get_search_method():
    print("\nChoose a search method:")
    print("1. Brute Force Search")
    print("2. Breadth First Search")
    print("3. Depth First Search")
    print("4. Iterative Deepening Depth First Search")
    print("5. Best First Search")
    print("6. A* Search")

    choice = input("Enter the number of your choice (1-6): ")

    if choice.isdigit() and int(choice) in {1, 2, 3, 4, 5, 6}:
        return int(choice)
    else:
        print("Invalid input. Please try again.")
        return get_search_method()

def run_search(graph, start_city, goal_city):
    choice = get_search_method()

    if choice == 1:
        print("/nRunning Brute Force Search..")
        result = brute_force_search(graph, start_city, goal_city)
    elif choice == 2:
        print("/nRunning Breadth First Search..")
        result = bfs(graph, start_city, goal_city)
    elif choice == 3:
        print("/nRunning Depth First Search..")
        result = dfs_search(graph, start_city, goal_city)
    elif choice == 4:
        print("/nRunning Iterative Deepening Depth First Seartch..")
        result = iddfs_search(graph, start_city, goal_city)
    elif choice == 5:
        print("/nRunning Best First Search..")
        result = best_first_search(graph, start_city, goal_city)
    elif choice == 6:
        print("/nRunning A* Search..")
        result = a_star_search(graph, start_city, goal_city)

    if result:
        print(f"Route found: {result}")
    else:
        print("No route found.")
        return run_search

# Main program to run the search
if __name__ == "__main__":
    # Example of how to call the run_search function:
    start_city = input("Enter the start city: ")
    goal_city = input("Enter the goal city: ")

    if start_city in coordinates and goal_city in coordinates:
        run_search(graph, start_city, goal_city)
    else:
        print("One or both cities not found in the data.")
