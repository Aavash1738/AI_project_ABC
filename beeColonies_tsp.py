from random import uniform, randint, sample
import time
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

def visualize_distance_matrix(distance_matrix):
    G = nx.Graph()

    num_nodes = len(distance_matrix)
    for i in range(num_nodes):
        G.add_node(i)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = distance_matrix[i][j]
            G.add_edge(i, j, weight=weight)

    pos = nx.spring_layout(G, scale=4)
    
    nx.draw_networkx_nodes(G, pos, node_size=180, alpha=0.8, node_color='yellow')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.8, label=True)
    nx.draw_networkx_labels(G, pos, font_size=13, font_color='black')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, alpha=0.9, font_size=12)
    
    plt.show()


a = time.time()

# distanceMatrix = [
# [0 , 10 , 15 , 20 , 8], 
# [10 , 0 , 5 , 12 , 18],
# [15 , 5 , 0 , 9 , 13 ],
# [20 , 12 , 9 , 0 , 6 ],
# [8 , 18 , 13 , 6 , 0 ]]

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

# distanceMatrix = [
#     [0, 29, 20, 21, 17, 28, 23, 29, 31, 30],
#     [29, 0, 15, 17, 28, 40, 20, 25, 30, 24],
#     [20, 15, 0, 35, 25, 30, 28, 36, 20, 28],
#     [21, 17, 35, 0, 27, 29, 23, 29, 27, 26],
#     [17, 28, 25, 27, 0, 29, 25, 32, 23, 24],
#     [28, 40, 30, 29, 29, 0, 32, 34, 36, 40],
#     [23, 20, 28, 23, 25, 32, 0, 22, 24, 25],
#     [29, 25, 36, 29, 32, 34, 22, 0, 22, 26],
#     [31, 30, 20, 27, 23, 36, 24, 22, 0, 27],
#     [30, 24, 28, 26, 24, 40, 25, 26, 27, 0]
# ]


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

visualize_distance_matrix(distanceMatrix)