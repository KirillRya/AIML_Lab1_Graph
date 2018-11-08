from queue import Queue
import heapq

dictionary = {}
distances = {}


def takedistance(x1, x2, y1, y2):
    return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** .5


def input(dictionary, distances):
    for line in open('l1_points.txt'):
        # for line in open('t2.txt'):
        line = line.split('\n')
        line = line[0]
        line = line.split(',')
        line[1] = int(line[1])
        line[2] = int(line[2])
        dictionary[line[0]] = line[1:]

    for line in open('l1_links.txt'):
        # for line in open('t1.txt'):
        line = line.split('\n')
        line = line[0]
        line = line.split(',')
        dist = takedistance(dictionary[line[0]][0], dictionary[line[1]][0], dictionary[line[0]][1],
                            dictionary[line[1]][1])
        distances[line[0], line[1]] = dist
        distances[line[1], line[0]] = dist


def dfsmain(start, finish):
    visited = list()
    cost = [0]

    def dfs(start, finish, cost):
        if start == finish:
            visited.append(start)
            return
        if start in visited:
            return
        visited.append(start)
        for i, j in distances.items():
            if i[0] == start and visited[-1] != finish:
                if not i[1] in visited:
                    cost[0] += j
                    dfs(i[1], finish, cost)

    dfs(start, finish, cost)
    print("DFS:")
    printAll(start, finish, visited, cost[0])


def bfsmain(start, finish):
    cost = [0]
    visited = list()
    queue = Queue()
    queue.put(start)

    def bfs(start, finish, cost):
        while not queue.empty():
            queue.get(0)
            if start == finish:
                visited.append(finish)
                queue.queue.clear()
                break
            if start in visited:
                return
            visited.append(start)
            for j in distances.items():
                if j[0][0] == start and not j[0][1] in visited:
                    cost[0] += j[1]
                    queue.put(j[0][1])
            while queue:
                bfs(queue.queue[0], finish, cost)
                if queue.qsize() == 0:
                    break
        return visited

    visited = bfs(start, finish, cost)
    print("BFS:")
    printAll(start, finish, visited, cost[0])


def ucsmain(start, finish):
    h = [(0, start)]
    visited = []
    cost = 0

    def ucs(start, finish, cost):
        while not h == []:
            start = heapq.heappop(h)
            cost += start[0]
            start = start[1]
            visited.append(start)
            if start == finish:
                return visited, cost
            for j in distances.items():
                if j[0][0] == start and not j[0][1] in visited:
                    heapq.heappush(h, (j[1], j[0][1]))

    visited, cost = ucs(start, finish, cost)
    print("UCS:")
    printAll(start, finish, visited, cost)


def a_starmain(start, finish):
    f = []
    h = {}
    g = [(0, start)]
    visited = []
    cost = 0

    def a_star(start, finish, cost):
        while not g == []:
            start = heapq.heappop(g)
            cost += start[0]
            start = start[1]
            visited.append(start)
            if start == finish:
                return visited, cost
            for j in distances.items():
                if j[0][0] == start and not j[0][1] in visited:
                    heapq.heappush(f, (j[1], j[0][1]))
                    h[j[0][1]] = takedistance((dictionary[j[0][1]])[0], dictionary[finish][0],
                                              ((dictionary[j[0][1]])[1]), dictionary[finish][1])
                    heapq.heappush(g, (h[j[0][1]] + j[1], j[0][1]))

    visited, cost = a_star(start, finish, cost)
    print("A*:")
    printAll(start, finish, visited, cost)


def printAll(start, finish, visited, cost):
    print("Way from", start, "to", finish, "is", visited)
    print("Num of visited points is", len(visited))
    print("Cost is", cost)
    print()


def test():
    start = "A"
    finish = "Z"

    input(dictionary, distances)
    dfsmain(start, finish)
    bfsmain(start, finish)
    ucsmain(start, finish)
    a_starmain(start, finish)


test()