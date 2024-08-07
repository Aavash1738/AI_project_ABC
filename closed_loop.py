import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from distMat import distancer

pos = 0

def visualize_distance_matrix(distance_matrix, path=None, ax=None):
    G = nx.Graph()

    num_nodes = len(distance_matrix)
    for i in range(num_nodes):
        G.add_node(i)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = distance_matrix[i][j]
            G.add_edge(i, j, weight=weight)

    global pos
    if not(pos):
        pos = nx.spring_layout(G, scale=4)
    
    nx.draw_networkx_nodes(G, pos, node_size=180, alpha=0.8, node_color='yellow', ax=ax)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.6, label=True, ax=ax, style='dashed', edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=13, font_color='black', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, alpha=0.9, font_size=10, ax=ax)

    if path is not None:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5, edge_color='green', alpha=0.8, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, alpha=0.9, font_size=12, ax=ax)

# Distance matrix (TSP dataset)
distanceMatrix = distancer()

def calculateCost(solution):
    totalDistance = 0
    index = solution[0]
    for nextIndex in solution[1:]:
        totalDistance += distanceMatrix[index][nextIndex]
        index = nextIndex
    totalDistance += distanceMatrix[index][solution[0]]  # Return to the start
    return totalDistance

def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]

def randF():
    return random.uniform(0.0001, 0.9999)

def rouletteSelection(bees):
    total = sum(1 / float(bees[i][1]) for i in range(len(bees)))
    probability = []
    section = 0
    for i in range(len(bees)):
        section += float((1 / bees[i][1]) / total)
        probability.append(section)
    nextGeneration = []
    for i in range(numFeeds):
        choice = randF()
        for j in range(len(probability)):
            if choice <= probability[j]:
                nextGeneration.append(bees[j])
                break
    return random.sample(nextGeneration, numFeeds)

def approachToGood(bees, a, b, c):
    bees = bees[0][:]
    swap(bees, a, b)
    swap(bees, b, c)
    return (bees, calculateCost(bees))

def removeBees(bees):
    bees = bees[0][:]
    indices = random.sample(range(n), 4)
    swap(bees, indices[0], indices[1])
    swap(bees, indices[1], indices[2])
    swap(bees, indices[2], indices[3])
    return (bees, calculateCost(bees))

# Parameters
numBees = len(distanceMatrix)
workerBees = 5
iteration = 100
numFeeds = 5
limitsOfTry = 5
n = len(distanceMatrix)
bees = []
firstPath = list(range(1, n))  # Start from node 1 to n-1 (excluding 0)

# Initialize bees
for i in range(numBees):
    path = [0] + random.sample(firstPath, n - 1) + [0]  # Start and end at node 0
    bees.append((path, calculateCost(path)))
bees.sort(key=lambda x: x[1])

a = time.time()

# Main algorithm loop
while iteration != 0:
    count = 0
    bestBees = bees[random.randint(0, int(2 + ((randF() - 0.5) * 2) * (2.5 - 1.2)))]
    for j in range(0, n):
        morePowerBees = approachToGood(bestBees, random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1))
        if bees[j][1] > morePowerBees[1]:
            bees[j] = morePowerBees
        else:
            limitsOfTry += 1
    bees.sort(key=lambda x: x[1])
    for i in range(numBees - workerBees, numBees):
        observer = rouletteSelection(bees)
        for l in range(workerBees, numBees):
            bees[l] = observer[count]
    count += 1
    if count > limitsOfTry:
        for k in range(n):
            bees[k] = removeBees(bees[k])
    bees.sort(key=lambda x: x[1])
    iteration -= 1

b = time.time()

# Include return to starting point in the output
best_path = bees[0][0]
print("Best path: ", best_path)
print("Best cost: ", bees[0][1])
print("Algorithm runtime: ", b - a)

fig, axes = plt.subplots(1, 2, figsize=(15, 7))

visualize_distance_matrix(distanceMatrix, ax=axes[0])
axes[0].set_title('Graph without path')

# Plot with the path
visualize_distance_matrix(distanceMatrix, path=bees[0][0], ax=axes[1])
axes[1].set_title('Graph with path')

#plt.show()