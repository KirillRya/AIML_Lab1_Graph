from collections import deque
import heapq
import copy

dictionary = {}
distances = {}


def takedistance(x1, x2, y1, y2):
    return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** .5


def input_dict(dictionary, distances):
    for line in open('l1_points.txt'):
        # for line in open('t2.txt'):
        line = line.rstrip()
        line = line.split(',')
        line[1] = int(line[1])
        line[2] = int(line[2])
        dictionary[line[0]] = line[1:]

    for line in open('l1_links.txt'):
        # for line in open('t1.txt'):
        line = line.rstrip()
        line = line.split(',')
        dist = takedistance(dictionary[line[0]][0], dictionary[line[1]][0], dictionary[line[0]][1],
                            dictionary[line[1]][1])
        if line[0] in distances:
            distances[line[0]].append((line[1],dist))
        else:
            distances[line[0]] = [(line[1],dist)]
        if line[1] in distances:
            distances[line[1]].append([line[0],dist])
        else:
            distances[line[1]] = [(line[0],dist)]


def dfsmain(start, finish):
    visited_final = list()
    visited = list()
    cost = [0]

    def dfs(start, finish, cost):
        if start == finish:
            visited_final.append(start)
            visited.append(start)
            return
        if start in visited:
            return
        visited_final.append(start)
        visited.append(start)
        for next_point,current_cost in distances.get(start):
            if  not visited[-1] == finish:
                if not next_point in visited:
                    cost[0] += current_cost
                    dfs(next_point, finish, cost)
        if not visited[-1] == finish:
            visited_final.remove(start)

    dfs(start, finish, cost)
    print("DFS:")
    printAll(start, finish, visited_final, visited, cost[0])


def bfsmain(start, finish):
    cost = [0]
    visited_final = list()
    visited = list()
    queue = deque(start)

    def bfs(start, finish, cost):
        flag_delete = True
        while not queue.__len__() == 0:
            queue.popleft()
            if start == finish:
                visited.append(finish)
                visited_final.append(finish)
                make_short_way(visited_final,finish)
                queue.clear()
                break
            if start in visited:
                return
            visited.append(start)
            visited_final.append(start)
            for next_point,current_cost in distances.get(start):
                if not next_point in visited:
                    flag_delete = False
                    cost[0] += current_cost
                    queue.append(next_point)
            if flag_delete == True:
                visited_final.remove(start)
            while queue:
                bfs(queue[0], finish, cost)
                if queue.__len__() == 0:
                    break
        return

    bfs(start, finish, cost)
    print("BFS:")
    printAll(start, finish, visited_final, visited, cost[0])


def ucsmain(start, finish):
    h = [(0, start)]
    visited = []
    cost = 0
    visited_final = []

    def ucs(start, finish, cost):
        while not h == []:
            start = heapq.heappop(h)
            if not start[1] in visited:
                cost_current_way = start[0]
                start = start[1]
                visited.append(start)
                if start == finish:
                    visited_final=copy.deepcopy(visited)
                    return visited_final,cost_current_way
                for next_point,current_cost in distances.get(start):
                    if not next_point in visited:
                        heapq.heappush(h, (current_cost + cost_current_way, next_point))

    visited_final,cost = ucs(start, finish, cost)
    make_short_way(visited_final, finish)
    print("UCS:")
    printAll(start, finish, visited_final, visited, cost)


def a_starmain(start, finish):
    f = []
    h = {start:0}
    g = [(0, start)]
    visited = []
    visited_final = []
    cost = 0

    def a_star(start, finish, cost):
        heuristic = 0
        while not g == []:
            start = heapq.heappop(g)
            cost += start[0]-h.get(start[1])
            start = start[1]
            visited.append(start)
            if start == finish:
                visited_final=copy.deepcopy(visited)
                return visited_final,cost
            for next_point,current_cost in distances.get(start):
                if not next_point in visited:
                    heapq.heappush(f, (current_cost, next_point))
                    point_begin_x,point_begin_y = dictionary[next_point]
                    point_end_x, point_end_y = dictionary[finish]
                    heuristic = takedistance(point_begin_x, point_end_x, point_begin_y, point_end_y)
                    h[next_point] = heuristic
                    heapq.heappush(g, (heuristic  + current_cost, next_point))

    visited_final,cost = a_star(start, finish, cost)
    make_short_way(visited_final, finish)
    print("A*:")
    printAll(start, finish, visited_final, visited, cost)


def make_short_way(visited,finish):
    visited_final = visited
    for next_point in reversed(visited_final):
        flag_delete = True
        if next_point == finish:
            pass
        else:
            for point in distances.get(next_point):
                if finish in point:
                    flag_delete = False
                    finish = next_point
                    break
            if flag_delete == True:
                visited_final.remove(next_point)
    return visited_final


def printAll(start, finish, visited_final, visited_full, cost):
    print("Way from", start, "to", finish, "is", visited_final)
    print("Full way is",visited_full)
    print("Num of visited points is", len(visited_full))
    print("Cost is", cost)
    print()


def test():
    start = "A"
    finish = "Z"

    input_dict(dictionary, distances)
    dfsmain(start, finish)
    bfsmain(start, finish)
    ucsmain(start, finish)
    a_starmain(start, finish)


test()