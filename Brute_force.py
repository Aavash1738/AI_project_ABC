from itertools import permutations

distanceMatrix = [
    [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80],
    [10, 0, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90],
    [15, 12, 0, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86],
    [20, 18, 14, 0, 16, 22, 28, 34, 40, 46, 52, 58, 64, 70, 76, 82],
    [25, 24, 20, 16, 0, 18, 26, 34, 42, 50, 58, 66, 74, 82, 90, 98],
    [30, 30, 26, 22, 18, 0, 20, 40, 50, 60, 70, 80, 90, 100, 110, 120],
    [35, 36, 32, 28, 26, 20, 0, 32, 44, 56, 68, 80, 92, 104, 116, 128],
    [40, 42, 38, 34, 34, 40, 32, 0, 38, 76, 114, 152, 190, 228, 266, 304],
    [45, 48, 44, 40, 42, 50, 44, 38, 0, 56, 112, 168, 224, 280, 336, 392],
    [50, 54, 50, 46, 50, 60, 56, 76, 56, 0, 70, 140, 210, 280, 350, 420],
    [55, 60, 56, 52, 58, 70, 68, 114, 112, 70, 0, 120, 240, 360, 480, 600],
    [60, 66, 62, 58, 66, 80, 80, 152, 168, 140, 120, 0, 240, 480, 720, 960],
    [65, 72, 68, 64, 74, 90, 92, 190, 224, 210, 240, 240, 0, 600, 1200, 1800],
    [70, 78, 74, 70, 82, 100, 104, 228, 280, 280, 360, 480, 600, 0, 1200, 1800],
    [75, 84, 80, 76, 90, 110, 116, 266, 336, 350, 480, 720, 1200, 1200, 0, 1200],
    [80, 90, 86, 82, 98, 120, 128, 304, 392, 420, 600, 960, 1800, 1800, 1200, 0]
]

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
