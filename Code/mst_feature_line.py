# Implementation of Kruskal's minimum spanning tree for breakline generation
import math

def take_second(elem):
    return elem[1]

def generate_mst(edge_list):
    edge_list.sort(key = take_second)

    vertices = []
    for e in edge_list:
        vertices.append(e[0][0])
        vertices.append(e[0][1])
    vertices = list(set(vertices))
    v_len = len(vertices)
    print(vertices)

    wqu = [[edge_list[0][0][0], edge_list[0][0][1]]] # weighted quick union
    min_tree = [[edge_list[0][0][0], edge_list[0][0][1]]]

    i = 1
    while (i < len(edge_list)):
        flag1 = 0
        i1 = 0
        while (i1 < len(wqu)):
            if wqu[i1].__contains__(edge_list[i][0][0]) == True:
                if wqu[i1].__contains__(edge_list[i][0][1]) == True:
                    flag1 = 1
                else:
                    # search edge_list[i][0][1] in other WQU lists
                    union_iter = i1
                    temp2 = -1
                    i2 = 0
                    while (i2 < len(wqu)):
                        if i2 != union_iter:
                            if wqu[i2].__contains__(edge_list[i][0][1]) == True:
                                temp2 = i2
                                break
                        i2 = i2 + 1
                    if temp2 != -1:
                        if len(wqu[temp2]) <= len(wqu[i1]):
                            for j in wqu[temp2]:
                                wqu[i1].append(j)
                            min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
                            del wqu[temp2]
                            flag1 = 1
                        else:
                            for j in wqu[i1]:
                                wqu[temp2].append(j)
                            min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
                            del wqu[i1]
                            flag1 = 1
                        
                    else:
                        wqu[i1].append(edge_list[i][0][1])
                        min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
                        flag1 = 1

            elif wqu[i1].__contains__(edge_list[i][0][1]) == True:
                # search edge_list[i][0][0] in other WQU lists
                union_iter = i1
                temp2 = -1
                i2 = 0
                while (i2 < len(wqu)):
                    if i2 != union_iter:
                        if wqu[i2].__contains__(edge_list[i][0][0]) == True:
                            temp2 = i2
                            break
                    i2 = i2 + 1
                if temp2 != -1:
                    if len(wqu[temp2]) <= len(wqu[i1]):
                        for j in wqu[temp2]:
                            wqu[i1].append(j)
                        min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
                        del wqu[temp2]
                        flag1 = 1
                    else:
                        for j in wqu[i1]:
                            wqu[temp2].append(j)
                        min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
                        del wqu[i1]
                        flag1 = 1
                
                else:
                    wqu[i1].append(edge_list[i][0][0])
                    min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
                    flag1 = 1
            
            if flag1 == 1:
                break
            else:
                i1 = i1 + 1

        if i1 == len(wqu):
            wqu.append([edge_list[i][0][0], edge_list[i][0][1]])
            min_tree.append([edge_list[i][0][0], edge_list[i][0][1]])
        
        if len(min_tree) >= v_len - 1:
            break
        i = i + 1
    #print('i: ', i)
    return min_tree #, wqu

"""edge_s = []
edge_s.append([[1, 2], 3])
edge_s.append([[1, 3], 3.16])
edge_s.append([[2, 3], 1])
edge_s.append([[2, 4], 2.8])
edge_s.append([[2, 5], 2])
edge_s.append([[2, 6], 1.4])
edge_s.append([[3, 5], 2.8])
edge_s.append([[3, 6], 1.72])
edge_s.append([[4, 5], 1])
edge_s.append([[4, 6], 2.72])
edge_s.append([[5, 6], 1.73])

result_tree = generate_mst(edge_s)
for i in result_tree:
    print(i)"""
