from itertools import permutations
from distMat import distancer


distanceMatrix = distancer()

def calculate_cost(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distanceMatrix[path[i]][path[i + 1]]
    return total_distance

def find_optimal_path(distanceMatrix):
    n = len(distanceMatrix)
    nodes = range(1, n)
    min_cost = float('inf')
    best_path = None

    for perm in permutations(nodes):
        path = (0,) + perm
        cost = calculate_cost(path)
        if cost < min_cost:
            min_cost = cost
            best_path = path

    return best_path, min_cost

optimal_path, optimal_cost = find_optimal_path(distanceMatrix)
print("Optimal path:", optimal_path)
print("Optimal cost:", optimal_cost)
