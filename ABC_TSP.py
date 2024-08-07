from random import uniform, randint, sample
import time
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
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

a = time.time()

distanceMatrix = distancer()

def cost(solution):  
    node = solution[0]
    distance = 0     
    for nextnode in solution[1:]:
        distance += distanceMatrix[node][nextnode]
        node = nextnode
    return distance 

def swap(sequence, i, j):  # change index of list
    temp = sequence[i]
    sequence[i] = sequence[j]  # changes index
    sequence[j] = temp

def randF():  # randomly protect number between 0-1
    return uniform(0.0001, 0.9999)

moveRandom = int(2 + ((randF() - 0.5) * 2) * (2.5 - 1.2))  
#moveRandom = int(randint(0,3))

def roulette(bees): 
    total = 0
    section = 0
    for i in range(len(bees)):
        total += (1 / float(bees[i][1]))  
    probability = []  
    for i in range(len(bees)):
        section += float((1 / int(bees[i][1])) / total) 
        probability.append(section)  
    nextGeneration = []  
    for i in range(numOnlookerBees):  
        choice = randF()  
        for j in range(len(probability)):
            if (choice <= probability[j]):
                nextGeneration.append(bees[j])
                break
    temp = sample(nextGeneration, numOnlookerBees) 
    nextGeneration = temp
    return nextGeneration

def two_opt(solution):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(solution) - 2):  
            for j in range(i + 2, len(solution)):
                new_solution = solution[:]
                new_solution[i:j] = reversed(new_solution[i:j])
                new_cost = cost(new_solution)
                if new_cost < cost(solution):
                    solution = new_solution
                    improved = True
    return solution

def goodness(bees, a, b, c):
    bees = bees[0][:]
    swap(bees, a, b)
    swap(bees, b, c)
    bees = two_opt(bees)  # Apply 2-opt local search
    return (bees, cost(bees))

def removeBees(bees):  
    bees = bees[0][:]
    num1 = randint(1, n - 1)
    num2 = randint(1, n - 1)
    num3 = randint(1, n - 1)
    num4 = randint(1, n - 1)
    swap(bees, num1, num2)
    swap(bees, num2, num3)
    swap(bees, num3, num4)
    return (bees, cost(bees))  


numBees = len(distanceMatrix) #usually a multiple (2-10) of number of nodes
n = len(distanceMatrix)
iteration = 100 

numEmployedBees = 5 
numOnlookerBees = 5
limitsOfTry = 5
  
bees = []  

firstPath = list(range(1, n))  
for i in range(numBees):  
    path = sample(firstPath, n - 1)
    path = [0] + path  
    bees.append((path, cost(path)))
bees.sort(key=itemgetter(1))  

initial_cost = cost(bees[0][0])

best_solution = bees[0][0]
best_cost = bees[0][1]

while (iteration != 0):
    count = 0  
    selectedBees = bees[randint(0, moveRandom)]  
    for j in range(0, n-1):
        betterBees = goodness(selectedBees, randint(1, n - 1), randint(1, n - 1), randint(1, n - 1))  
        if (bees[j][1] > betterBees[1]):  
            bees[j] = betterBees  
        else:
            limitsOfTry += 1 
    bees.sort(key=itemgetter(1)) 

    if bees[0][1] < best_cost:
        best_solution = bees[0][0]
        best_cost = bees[0][1]

    for i in range(numBees - numEmployedBees, numBees):
        observer = roulette(bees)  
        for l in range(numEmployedBees, numBees):
            bees[l] = observer[count]  
    count += 1
    if (count > limitsOfTry):  
        for k in range(n):
            bees[k] = removeBees(bees[k])  
    bees.sort(key=itemgetter(1))  
    iteration -= 1

b = time.time()
print("Best way: ", bees[0][0])
print("Best cost: ", bees[0][1])
print("Algorithm running time: ", b - a)

print("Initial cost:", initial_cost)
print("Final cost:", bees[0][1])
improvement = initial_cost - bees[0][1]
print("Fitness improvement:", improvement)

fig, axes = plt.subplots(1, 2, figsize=(15, 7))

# Plot without the path
visualize_distance_matrix(distanceMatrix, ax=axes[0])
axes[0].set_title('Graph without path')

# Plot with the path
visualize_distance_matrix(distanceMatrix, path=bees[0][0], ax=axes[1])
axes[1].set_title('Graph with path')

plt.show()