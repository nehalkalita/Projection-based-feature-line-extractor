#import numpy as np
import math
#from numba import jit
import sys
import csv
import multiprocessing
import os
import random
import mst_breakline
#os.environ["OPENBLAS_MAIN_FREE"] = "1"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pts_default = [] # imported processed points without thickness
grid_dim = [] # grid size as per resolution by dim value
grid_final = []
joined_ngbr_h = [] # stores information on joined neighbours
joined_ngbr_l = [] # stores information on joined neighbours
breaklines_mst = [] # breaklines after MST is applied
breaklines_mst_uq = [] # stores unique vertices of each breakline
breaklines_mst_ext = [] # stores exterior vertices of each breakline

def detect_mst(mst_index, mst_multi):
    for k in range(len(mst_index)):
        mst_multi[k] = mst_breakline.generate_mst(mst_multi[k])
    return mst_index, mst_multi

def get_mst(result_mst):
    global breaklines_mst
    
    for k in range(len(result_mst[0])):
        breaklines_mst[result_mst[0][k]] = result_mst[1][k]

def detect_uq(uq_index, uq_multi):
    detect_uq_v = []
    for i1 in range(len(uq_index)):
        detect_uq_v.append([])
        for i2 in range(len(uq_multi[i1])):
            if detect_uq_v[i1].__contains__(uq_multi[i1][i2][0]) == False:
                detect_uq_v[i1].append(uq_multi[i1][i2][0])
            if detect_uq_v[i1].__contains__(uq_multi[i1][i2][1]) == False:
                detect_uq_v[i1].append(uq_multi[i1][i2][1])
    return uq_index, detect_uq_v

def get_uq(result_uq):
    global breaklines_mst_uq

    for k in range(len(result_uq[0])):
        breaklines_mst_uq[result_uq[0][k]] = result_uq[1][k]

def detect_ext(ext_index, ext_multi, ext_uq):
    detect_ext_v = []
    for i1 in range(len(ext_index)):
        detect_ext_v.append([])
        for i2 in range(len(ext_uq[i1])):
            temp1 = 0
            for i3 in range(len(ext_multi[i1])):
                if ext_uq[i1][i2] == ext_multi[i1][i3][0] or ext_uq[i1][i2] == ext_multi[i1][i3][1]:
                    temp1 = temp1 + 1
            if temp1 == 1:
                detect_ext_v[i1].append(ext_uq[i1][i2])
    return ext_index, detect_ext_v

def get_ext(result_ext):
    global breaklines_mst_ext

    for k in range(len(result_ext[0])):
        breaklines_mst_ext[result_ext[0][k]] = result_ext[1][k]

def clear_variables():
    global pts_default
    global grid_dim
    global grid_final
    global joined_ngbr_h, joined_ngbr_l
    global breaklines_mst
    global breaklines_mst_uq
    global breaklines_mst_ext

    pts_default = []
    grid_dim = []
    grid_final = []
    joined_ngbr_h = []
    joined_ngbr_l = []
    breaklines_mst = []
    breaklines_mst_uq = []
    breaklines_mst_ext = []

def join_neighbors(total_cores, temp_loc, dim, blk_sp, mn_pxy, mx_nbr, mx_lp, only_p, only_e, d_places, en_x, en_y, en_z, xyz_return):
    grids = open(resource_path('grid_n_decimal.csv'), 'r')
    limits = open(resource_path('Limits.csv'), 'r')
    dim = int(dim)
    blk_span_r = blk_sp
    
    min_p_length = mn_pxy
    max_length = mx_nbr
    max_length = float(max_length)
    
    min_p_length = float(min_p_length)
    if min_p_length < max_length:
        min_p_length = max_length

    max_loop_length = mx_lp
    max_loop_length = float(max_loop_length)
    if max_loop_length > max_length:
        max_loop_length = max_length

    total_cores = int(total_cores)
        
    final_fname = temp_loc + 'F'
    fname = ''
    fname = fname + '_' + str(dim) + '_' + str(blk_span_r)    
    fname = fname + '.csv'
    final_fname = final_fname + fname
    f1 = open(final_fname, 'r')   # format: y_x
    if only_p == 1:
        f2 = open(temp_loc + 'breakline_points.csv', 'w', newline='')
        csv_write1 = csv.writer(f2, delimiter = ',')
    if only_e == 1:
        f3 = open(temp_loc + 'breakline_edges.csv', 'w', newline='')
        csv_write2 = csv.writer(f3, delimiter = ',')
    f4 = open(temp_loc + 'breaklines.obj', 'w', newline='')
    r1 = csv.reader(f1)
    r2 = csv.reader(grids)
    r3 = csv.reader(limits)
    
    X_dim, Y_dim = 0, 0
    for line in r2:
        X_dim = int(line[1])
        Y_dim = int(line[2])
    grids.close()
    d_places = int(math.pow(10, d_places))

    Xs, Xl, Ys, Yl = 0, 0, 0, 0
    for line in r3:
        Xs = float(line[0]) * d_places   #since there are n digits after decimal
        Xl = float(line[1]) * d_places
        Ys = float(line[2]) * d_places
        Yl = float(line[3]) * d_places    
    Xs = int(Xs)
    Xl = int(Xl)
    Ys = int(Ys)
    Yl = int(Yl)
    
    global pts_default
    global grid_dim
    global grid_final
    global joined_ngbr_h
    global joined_ngbr_l
    pts_default = []
    grid_dim = []
    grid_final = []
    joined_ngbr_h = []
    joined_ngbr_l = []
    
    i = 0 
    while (i < X_dim * Y_dim): #25239 63998
        grid_dim.append([])
        grid_final.append([])
        joined_ngbr_h.append([])
        joined_ngbr_l.append([])
        i = i + 1
    
    for line in r1:
        pts_default.append([int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7])]) # 6 -> Y, 7 -> X
    f1.close()
    
    for i in range(len(pts_default)):
        temp1 = (pts_default[i][6] * X_dim) + pts_default[i][7]
        #print(temp1, len(grid_dim))
        if temp1 < len(grid_dim):
            if grid_dim[temp1] == []:
                if pts_default[i][3] == 255 and pts_default[i][4] == 0 and pts_default[i][5] == 0:
                    grid_dim[temp1].append(pts_default[i][0])
                    grid_dim[temp1].append(pts_default[i][1])
                    grid_dim[temp1].append(pts_default[i][2])
                    grid_dim[temp1].append(1)
                elif pts_default[i][3] == 0 and pts_default[i][4] == 169 and pts_default[i][5] == 51:
                    grid_dim[temp1].append(pts_default[i][0])
                    grid_dim[temp1].append(pts_default[i][1])
                    grid_dim[temp1].append(pts_default[i][2])
                    grid_dim[temp1].append(2)
                else: # 255,191,0
                    grid_dim[temp1].append(pts_default[i][0])
                    grid_dim[temp1].append(pts_default[i][1])
                    grid_dim[temp1].append(pts_default[i][2])
                    grid_dim[temp1].append(3)
            else:
                Xi = grid_dim[temp1][0]
                Yi = grid_dim[temp1][1]
                Zi = grid_dim[temp1][2]
                grid_dim[temp1][0] = round((Xi + pts_default[i][0]) / 2)
                grid_dim[temp1][1] = round((Yi + pts_default[i][1]) / 2)
                grid_dim[temp1][2] = round((Zi + pts_default[i][2]) / 2)
          
    # detect connectivity between points
    # on the basis each point's x,y distances from centre of their respective block

    breakline_cn = -1 # total number of breaklines
    cur_breakline_cn = -1 # current breakline number
    breakline_shared = [] # stores shared breaklines
    breakline_values = [] # stores list of breakline values
    i1 = 0
    while (i1 < Y_dim):
        i2 = 0
        while (i2 < X_dim):
            temp3 = (i1 * X_dim) + i2
            if grid_dim[temp3] != []:
                if int((grid_dim[temp3][0] - Xs - max_length) / dim) >= 0:
                    l_limit = int((grid_dim[temp3][0] - Xs - max_length) / dim)
                else:
                    l_limit = 0
                if int((grid_dim[temp3][0] - Xs + max_length) / dim) < X_dim:
                    r_limit = int((grid_dim[temp3][0] - Xs + max_length) / dim)
                else:
                    r_limit = X_dim - 1
                if int((grid_dim[temp3][1] - Ys - max_length) / dim) >= 0:
                    t_limit = int((grid_dim[temp3][1] - Ys - max_length) / dim)
                else:
                    t_limit = 0
                if int((grid_dim[temp3][1] - Ys + max_length) / dim) < Y_dim:
                    b_limit = int((grid_dim[temp3][1] - Ys + max_length) / dim)
                else:
                    b_limit = Y_dim - 1
                
                nbr_range = [] # range within which neighbors with 'max_length' can be obtained
                j = 0
                while (j < (b_limit - t_limit + 1) * (r_limit - l_limit + 1)):
                    nbr_range.append([])
                    j = j + 1
                
                # find points within range
                nbr_points = [] # stores positions where points are found
                j1 = t_limit
                while (j1 < i1):
                    j2 = l_limit
                    while (j2 <= r_limit):
                        temp4 = (j1 * X_dim) + j2
                        if grid_dim[temp4] != []:
                            if grid_dim[temp4][3] == 3 or (grid_dim[temp3][3] == grid_dim[temp4][3]):
                                if max_length >= math.sqrt(math.pow(grid_dim[temp3][0] - grid_dim[temp4][0], 2) + math.pow(grid_dim[temp3][1] - grid_dim[temp4][1], 2) + math.pow(grid_dim[temp3][2] - grid_dim[temp4][2], 2)):
                                    temp2 = ((j1 - t_limit) * (r_limit - l_limit + 1)) + (j2 - l_limit)
                                    nbr_points.append([j1 - t_limit, j2 - l_limit])
                                    for k in grid_dim[temp4]:
                                        nbr_range[temp2].append(k)
                                    nbr_range[temp2].append(j1)
                                    nbr_range[temp2].append(j2)
                        j2 = j2 + 1
                    j1 = j1 + 1
                j2 = l_limit
                while (j2 < i2):
                    temp4 = (j1 * X_dim) + j2
                    if grid_dim[temp4] != []:
                        if grid_dim[temp4][3] == 3 or (grid_dim[temp3][3] == grid_dim[temp4][3]):
                            if max_length >= math.sqrt(math.pow(grid_dim[temp3][0] - grid_dim[temp4][0], 2) + math.pow(grid_dim[temp3][1] - grid_dim[temp4][1], 2) + math.pow(grid_dim[temp3][2] - grid_dim[temp4][2], 2)):
                                temp2 = ((j1 - t_limit) * (r_limit - l_limit + 1)) + (j2 - l_limit)
                                nbr_points.append([j1 - t_limit, j2 - l_limit])
                                for k in grid_dim[temp4]:
                                    nbr_range[temp2].append(k)
                                nbr_range[temp2].append(j1)
                                nbr_range[temp2].append(j2)
                    j2 = j2 + 1
                j2 = j2 + 1
                while (j2 <= r_limit):
                    temp4 = (j1 * X_dim) + j2
                    if grid_dim[temp4] != []:
                        if grid_dim[temp4][3] == 3 or (grid_dim[temp3][3] == grid_dim[temp4][3]):
                            if max_length >= math.sqrt(math.pow(grid_dim[temp3][0] - grid_dim[temp4][0], 2) + math.pow(grid_dim[temp3][1] - grid_dim[temp4][1], 2) + math.pow(grid_dim[temp3][2] - grid_dim[temp4][2], 2)):
                                temp2 = ((j1 - t_limit) * (r_limit - l_limit + 1)) + (j2 - l_limit)
                                nbr_points.append([j1 - t_limit, j2 - l_limit])
                                for k in grid_dim[temp4]:
                                    nbr_range[temp2].append(k)
                                nbr_range[temp2].append(j1)
                                nbr_range[temp2].append(j2)
                    j2 = j2 + 1
                j1 = j1 + 1
                while (j1 <= b_limit):
                    j2 = l_limit
                    while (j2 <= r_limit):
                        temp4 = (j1 * X_dim) + j2
                        if grid_dim[temp4] != []:
                            if grid_dim[temp4][3] == 3 or (grid_dim[temp3][3] == grid_dim[temp4][3]):
                                if max_length >= math.sqrt(math.pow(grid_dim[temp3][0] - grid_dim[temp4][0], 2) + math.pow(grid_dim[temp3][1] - grid_dim[temp4][1], 2) + math.pow(grid_dim[temp3][2] - grid_dim[temp4][2], 2)):
                                    temp2 = ((j1 - t_limit) * (r_limit - l_limit + 1)) + (j2 - l_limit)
                                    nbr_points.append([j1 - t_limit, j2 - l_limit])
                                    for k in grid_dim[temp4]:
                                        nbr_range[temp2].append(k)
                                    nbr_range[temp2].append(j1)
                                    nbr_range[temp2].append(j2)
                        j2 = j2 + 1
                    j1 = j1 + 1

                if len(nbr_points) > 0:
                    # detect cur_breakline_cn value
                    if grid_final[temp3] != []:
                        list1 = [grid_final[temp3][0]]
                        k = 0
                        while (k < len(nbr_points)):
                            temp2 = (nbr_points[k][0] * (r_limit - l_limit + 1)) + nbr_points[k][1]
                            temp4 = (nbr_range[temp2][4] * X_dim) + nbr_range[temp2][5]

                            if grid_final[temp4] != []: # and type(grid_final[temp4][0]) == int:
                                if list1.__contains__(grid_final[temp4][0]) == False:
                                    list1.append(grid_final[temp4][0])
                            k = k + 1
                        if len(list1) == 1:
                            cur_breakline_cn = list1[0]
                        else:
                            list1.sort()
                            breakline_shared.append(list1)
                            cur_breakline_cn = list1[0]
                    else:
                        # VERIFY THIS LOGIC
                        list1 = []
                        k = 0
                        while (k < len(nbr_points)):
                            temp2 = (nbr_points[k][0] * (r_limit - l_limit + 1)) + nbr_points[k][1]
                            temp4 = (nbr_range[temp2][4] * X_dim) + nbr_range[temp2][5]

                            if grid_final[temp4] != []: # and type(grid_final[temp4][0]) == int:
                                if list1.__contains__(grid_final[temp4][0]) == False:
                                    list1.append(grid_final[temp4][0])
                            k = k + 1
                        if len(list1) == 0:
                            breakline_cn = breakline_cn + 1
                            cur_breakline_cn = breakline_cn
                            grid_final[temp3].append(cur_breakline_cn)
                            breakline_values.append(breakline_cn)
                        elif len(list1) == 1:
                            cur_breakline_cn = list1[0]
                            grid_final[temp3].append(cur_breakline_cn)
                        else:
                            list1.sort()
                            breakline_shared.append(list1)
                            cur_breakline_cn = list1[0]
                            grid_final[temp3].append(cur_breakline_cn)
                                        
                    k = 0
                    while (k < len(nbr_points)):
                        temp2 = (nbr_points[k][0] * (r_limit - l_limit + 1)) + nbr_points[k][1]
                        temp4 = math.sqrt(math.pow(grid_dim[temp3][0] - nbr_range[temp2][0], 2) + math.pow(grid_dim[temp3][1] - nbr_range[temp2][1], 2) + math.pow(grid_dim[temp3][2] - nbr_range[temp2][2], 2))
                        temp5 = (nbr_range[temp2][4] * X_dim) + nbr_range[temp2][5]
                        if grid_final[temp5] == []:
                            grid_final[temp5].append(cur_breakline_cn)
                            grid_final[temp5].append([temp3, temp4]) # [connecting point, distance]
                        else:
                            j1 = 1
                            while (j1 < len(grid_final[temp3])):
                                if grid_final[temp3][j1][0] == temp5:
                                    break
                                j1 = j1 + 1
                            if j1 == len(grid_final[temp3]):
                                j2 = 1
                                while (j2 < len(grid_final[temp5])):
                                    if grid_final[temp5][j2][0] == temp3:
                                        break
                                    j2 = j2 + 1
                                if j2 == len(grid_final[temp5]):
                                    grid_final[temp5].append([temp3, temp4]) # [connecting point, distance]
                        k = k + 1
            i2 = i2 + 1
        i1 = i1 + 1

    # join breaklines
    breakline_shared.sort()
    for j in range(2):
        i1 = 0
        while (i1 < len(breakline_shared) - 1):
            i2 = i1 + 1
            while (i2 < len(breakline_shared)):
                i3 = 0
                while (i3 < len(breakline_shared[i2])):
                    if breakline_shared[i1].__contains__(breakline_shared[i2][i3]) == True:
                        break
                    i3 = i3 + 1
                if i3 < len(breakline_shared[i2]):
                    k = 0
                    while (k < len(breakline_shared[i2])):
                        if breakline_shared[i1].__contains__(breakline_shared[i2][k]) == False:
                            breakline_shared[i1].append(breakline_shared[i2][k])
                        k = k + 1         
                    del breakline_shared[i2]
                else:
                    i2 = i2 + 1
            i1 = i1 + 1
    i1 = 0
    while (i1 < len(breakline_shared)):
        breakline_shared[i1].sort()
        i1 = i1 + 1
    k = 0
    while (k < len(breakline_values)):
        i1 = 0
        while (i1 < len(breakline_shared)):
            if breakline_shared[i1].__contains__(breakline_values[k]) == True:
                break
            i1 = i1 + 1
        if i1 < len(breakline_shared):
            del breakline_values[k]
        else:
            k = k + 1

    for k in breakline_values:
        if k < breakline_shared[0][0]:
            breakline_shared.insert(0, [k])
        elif k > breakline_shared[-1][0]:
            breakline_shared.append([k])
        else:
            i1 = 0
            while (i1 < len(breakline_shared) - 1):
                # [2,6]   [5,7]
                if k > breakline_shared[i1][0] and k < breakline_shared[i1 + 1][0]:
                    breakline_shared.insert(i1 + 1, [k])
                    break
                i1 = i1 + 1
    breakline_values = []

    global breaklines_mst
    breaklines_mst = []
    for k in range(len(breakline_shared)): # breakline_cn + 1
        breaklines_mst.append([])

    # add values to 'breaklines_mst'
    for i1 in range(len(grid_final)): # DOES NOT REQUIRE MULTI-PROCESSING
        # some locations only has breakline number
        if len(grid_final[i1]) > 1:
            k1 = 0
            while (k1 < len(breakline_shared)):
                if breakline_shared[k1].__contains__(grid_final[i1][0]) == True:
                    break
                k1 = k1 + 1
            #print(len(breaklines_mst), k1, grid_final[i1])
            for i2 in range(1, len(grid_final[i1])):
                breaklines_mst[k1].append([[i1, grid_final[i1][i2][0]], grid_final[i1][i2][1]])

    if total_cores > 1:
        if (len(breaklines_mst)) / total_cores >= 1: #breakline_cn + 1
            temp1_cores = total_cores
        else:
            temp1_cores = total_cores - 1
            while (temp1_cores >= 1):
                if (len(breaklines_mst)) / total_cores >= 1: #breakline_cn + 1
                    break
                else:
                    temp1_cores = total_cores - 1
        p = multiprocessing.Pool(temp1_cores)
        breaklines_mst_multi = [] # 'breaklines_mst' regrouped for multiprocessing 
        breaklines_mst_index = [] # stores the index values of each group
        for k in range(temp1_cores):
            breaklines_mst_multi.append([])
            breaklines_mst_index.append([])
            i1 = k
            while (i1 < len(breaklines_mst)): #breakline_cn + 1
                breaklines_mst_index[k].append(i1)
                breaklines_mst_multi[k].append(breaklines_mst[i1])
                i1 = i1 + temp1_cores
            p.apply_async(detect_mst, args=(breaklines_mst_index[k], breaklines_mst_multi[k]), callback=get_mst) 
        p.close()
        p.join()

    else:
        #print(breaklines_mst[1])
        for k in range(len(breaklines_mst)):
            breaklines_mst[k] = mst_breakline.generate_mst(breaklines_mst[k])

    #print(breaklines_mst[1])

    # remove wrong breaklines as per 'min_p_length'
    i1 = 0
    while (i1 < len(breaklines_mst)):
        if grid_dim[breaklines_mst[i1][0][0]][0] <= grid_dim[breaklines_mst[i1][0][1]][0]:
            temp_X_l = grid_dim[breaklines_mst[i1][0][0]][0]
            temp_X_r = grid_dim[breaklines_mst[i1][0][1]][0]
        else:
            temp_X_l = grid_dim[breaklines_mst[i1][0][1]][0]
            temp_X_r = grid_dim[breaklines_mst[i1][0][0]][0]
        if temp_X_r - temp_X_l >= min_p_length:
            i1 = i1 + 1
        else:
            if grid_dim[breaklines_mst[i1][0][0]][1] <= grid_dim[breaklines_mst[i1][0][1]][1]:
                temp_Y_t = grid_dim[breaklines_mst[i1][0][0]][1]
                temp_Y_b = grid_dim[breaklines_mst[i1][0][1]][1]
            else:
                temp_Y_t = grid_dim[breaklines_mst[i1][0][1]][1]
                temp_Y_b = grid_dim[breaklines_mst[i1][0][0]][1]
            if temp_Y_b - temp_Y_t >= min_p_length:
                i1 = i1 + 1
            else:
                i2 = 1
                while (i2 < len(breaklines_mst[i1])):
                    if grid_dim[breaklines_mst[i1][i2][0]][0] <= grid_dim[breaklines_mst[i1][i2][1]][0]:
                        if grid_dim[breaklines_mst[i1][i2][0]][0] < temp_X_l:
                            temp_X_l = grid_dim[breaklines_mst[i1][i2][0]][0]
                        if grid_dim[breaklines_mst[i1][i2][1]][0] > temp_X_r:
                            temp_X_r = grid_dim[breaklines_mst[i1][i2][1]][0]
                    else:
                        if grid_dim[breaklines_mst[i1][i2][1]][0] < temp_X_l:
                            temp_X_l = grid_dim[breaklines_mst[i1][i2][1]][0]
                        if grid_dim[breaklines_mst[i1][i2][0]][0] > temp_X_r:
                            temp_X_r = grid_dim[breaklines_mst[i1][i2][0]][0]
                    if temp_X_r - temp_X_l >= min_p_length:
                        break
                    else:
                        if grid_dim[breaklines_mst[i1][i2][0]][1] <= grid_dim[breaklines_mst[i1][i2][1]][1]:
                            if grid_dim[breaklines_mst[i1][i2][0]][1] < temp_Y_t:
                                temp_Y_t = grid_dim[breaklines_mst[i1][i2][0]][1]
                            if grid_dim[breaklines_mst[i1][i2][1]][1] > temp_Y_b:
                                temp_Y_b = grid_dim[breaklines_mst[i1][i2][1]][1]
                        else:
                            if grid_dim[breaklines_mst[i1][i2][1]][1] < temp_Y_t:
                                temp_Y_t = grid_dim[breaklines_mst[i1][i2][1]][1]
                            if grid_dim[breaklines_mst[i1][i2][0]][1] > temp_Y_b:
                                temp_Y_b = grid_dim[breaklines_mst[i1][i2][0]][1]
                        if temp_Y_b - temp_Y_t >= min_p_length:
                            break
                    i2 = i2 + 1
                if i2 < len(breaklines_mst[i1]):
                    i1 = i1 + 1
                else:
                    del breaklines_mst[i1]

    global breaklines_mst_uq
    global breaklines_mst_ext
    breaklines_mst_uq = []
    breaklines_mst_ext = []

    if total_cores > 1:
        for k in range(len(breaklines_mst)):
            breaklines_mst_uq.append([])
            breaklines_mst_ext.append([])
        if len(breaklines_mst) / total_cores >= 1:
            temp1_cores = total_cores
        else:
            temp1_cores = total_cores - 1
            while (temp1_cores >= 1):
                if (len(breaklines_mst)) / total_cores >= 1: #breakline_cn + 1
                    break
                else:
                    temp1_cores = total_cores - 1
        p = multiprocessing.Pool(temp1_cores)
        breaklines_uq_multi = []
        breaklines_uq_index = []
        for k in range(temp1_cores):
            breaklines_uq_multi.append([])
            breaklines_uq_index.append([])
            i1 = k
            while (i1 < len(breaklines_mst)):
                breaklines_uq_index[k].append(i1)
                breaklines_uq_multi[k].append(breaklines_mst[i1])
                i1 = i1 + temp1_cores
            p.apply_async(detect_uq, args=(breaklines_uq_index[k], breaklines_uq_multi[k]), callback=get_uq)
        p.close()
        p.join()
        del breaklines_uq_index
        del breaklines_uq_multi

        p = multiprocessing.Pool(temp1_cores)
        breaklines_ext_multi = []
        breaklines_ext_uq = []
        breaklines_ext_index = []
        for k in range(temp1_cores):
            breaklines_ext_multi.append([])
            breaklines_ext_uq.append([])
            breaklines_ext_index.append([])
            i1 = k
            while (i1 < len(breaklines_mst)):
                breaklines_ext_index[k].append(i1)
                breaklines_ext_multi[k].append(breaklines_mst[i1])
                breaklines_ext_uq[k].append(breaklines_mst_uq[i1])
                i1 = i1 + temp1_cores
            p.apply_async(detect_ext, args=(breaklines_ext_index[k], breaklines_ext_multi[k], breaklines_ext_uq[k]), callback=get_ext)
        p.close()
        p.join()
        
    else:
        for i1 in range(len(breaklines_mst)):
            breaklines_mst_uq.append([])
            for i2 in range(len(breaklines_mst[i1])):
                if breaklines_mst_uq[i1].__contains__(breaklines_mst[i1][i2][0]) == False:
                    breaklines_mst_uq[i1].append(breaklines_mst[i1][i2][0])
                if breaklines_mst_uq[i1].__contains__(breaklines_mst[i1][i2][1]) == False:
                    breaklines_mst_uq[i1].append(breaklines_mst[i1][i2][1])
                    
        for i1 in range(len(breaklines_mst)):
            breaklines_mst_ext.append([])
            for i2 in range(len(breaklines_mst_uq[i1])):
                temp1 = 0
                for i3 in range(len(breaklines_mst[i1])):
                    if breaklines_mst_uq[i1][i2] == breaklines_mst[i1][i3][0] or breaklines_mst_uq[i1][i2] == breaklines_mst[i1][i3][1]:
                        temp1 = temp1 + 1
                if temp1 == 1:
                    breaklines_mst_ext[i1].append(breaklines_mst_uq[i1][i2])

    # join loops in breaklines
    for i1 in range(len(breaklines_mst_ext)): # cannot use multiprocessing because entire 'grid_dim' needs to be passed
        i2 = 0
        while (i2 < len(breaklines_mst_ext[i1])):
            temp2 = [] # stores possible new edges with temp3 (include distances)
            temp3 = breaklines_mst_ext[i1][i2]
            flag1 = 0
            for j1 in range(len(breaklines_mst_uq[i1])):
                temp4 = breaklines_mst_uq[i1][j1]
                if temp3 != temp4:
                    temp5 = math.sqrt(math.pow(grid_dim[temp3][0] - grid_dim[temp4][0], 2) + math.pow(grid_dim[temp3][1] - grid_dim[temp4][1], 2) + math.pow(grid_dim[temp3][2] - grid_dim[temp4][2], 2))
                    if max_loop_length >= temp5:
                        j2 = 0
                        while (j2 < len(breaklines_mst[i1])):
                            if breaklines_mst[i1][j2] == [temp3, temp4] or breaklines_mst[i1][j2] == [temp4, temp3]:
                                break
                            j2 = j2 + 1
                        if j2 >= len(breaklines_mst[i1]):
                            temp2.append([temp3, temp4, temp5])
                            flag1 = 1
            if flag1 == 1:
                temp1 = [0, temp2[0][2]]
                for k in range(1, len(temp2)):
                    if temp1[1] > temp2[k][2]:
                        #if temp1[1] < temp2[k][2]:
                        temp1 = [k, temp2[k][2]]
                breaklines_mst[i1].append([temp2[temp1[0]][0], temp2[temp1[0]][1]])
                del breaklines_mst_ext[i1][i2] # NEEDS CORRECTION
            else:
                i2 = i2 + 1
    
    xyz_pos = []
    if en_x < en_y:
        if en_y < en_z:
            xyz_pos = [0, 1, 2]
        else:
            xyz_pos = [0, 2, 1]
    elif en_y < en_x:
        if en_x < en_z:
            xyz_pos = [1, 0, 2]
        else:
            xyz_pos = [1, 2, 0]
    elif en_z < en_x:
        if en_x < en_y:
            xyz_pos = [2, 0, 1]
        else:
            xyz_pos = [2, 1, 0]

    if only_p == 1:
        i1 = 0
        while (i1 < len(breaklines_mst_uq)):
            i2 = 0
            while (i2 < len(breaklines_mst_uq[i1])):
                temp1 = breaklines_mst_uq[i1][i2]
                csv_write1.writerow([str(round((grid_dim[temp1][xyz_pos[0]] / d_places) - xyz_return[xyz_pos[0]], 2)), str(round((grid_dim[temp1][xyz_pos[1]] / d_places) - xyz_return[xyz_pos[1]], 2)), str(round((grid_dim[temp1][xyz_pos[2]] / d_places) - xyz_return[xyz_pos[2]], 2))])
                """if grid_dim[temp1][3] == 1:
                    csv_write1.writerow([str(round(grid_dim[temp1][0] / d_places, 2)), str(round(grid_dim[temp1][1] / d_places, 2)), str(round(grid_dim[temp1][2] / d_places, 2)), str(255), str(0), str(0)])
                elif grid_dim[temp1][3] == 2:
                    csv_write1.writerow([str(round(grid_dim[temp1][0] / d_places, 2)), str(round(grid_dim[temp1][1] / d_places, 2)), str(round(grid_dim[temp1][2] / d_places, 2)), str(0), str(169), str(51)])
                elif grid_dim[temp1][3] == 3:
                    csv_write1.writerow([str(round(grid_dim[temp1][0] / d_places, 2)), str(round(grid_dim[temp1][1] / d_places, 2)), str(round(grid_dim[temp1][2] / d_places, 2)), str(255), str(191), str(0)])"""
                i2 = i2 + 1
            i1 = i1 + 1
        f2.close()
        
    if only_e == 1: # x1, y1, z1, x2, y2, z2, i1
        for i1 in range(len(breaklines_mst)):
            for i2 in range(len(breaklines_mst[i1])):
                temp1, temp2 = breaklines_mst[i1][i2][0], breaklines_mst[i1][i2][1]
                list_temp = []
                for i3 in range(3):
                    #list_temp.append(str(round(grid_dim[temp1][i3] / d_places, 2)))
                    list_temp.append(str(round((grid_dim[temp1][xyz_pos[i3]] / d_places) - xyz_return[xyz_pos[i3]], 2)))
                for i3 in range(3):
                    list_temp.append(str(round((grid_dim[temp2][xyz_pos[i3]] / d_places) - xyz_return[xyz_pos[i3]], 2)))
                list_temp.append(str(i1))
                csv_write2.writerow(list_temp)
        f3.close()

    # store edges in the OBJ file
    breaklines_uq_pos = [] # [starting position, total]
    count_points = 1
    for k in range(len(breaklines_mst_uq)):
        breaklines_uq_pos.append([count_points, len(breaklines_mst_uq[k])])
        count_points = count_points + len(breaklines_mst_uq[k])
        
    f4.write('# Edges for data parameters: ' + str(dim) + ' ' + str(blk_span_r) + ' ' + str(min_p_length) + ' ' + str(max_length) + ' ' + str(max_loop_length) + '\n\n')
    f4.write('g\n')
    for i1 in range(len(breaklines_mst_uq)):
        R1 = random.randint(0, 255)
        G1 = random.randint(0, 255)
        B1 = random.randint(0, 255)
        R1 = R1 / 255
        G1 = G1 / 255
        B1 = B1 / 255
        for i2 in range(len(breaklines_mst_uq[i1])):
            #f4.write('v ' + str(round(grid_dim[breaklines_mst_uq[i1][i2]][0] / d_places, 2)) + ' ' + str(round(grid_dim[breaklines_mst_uq[i1][i2]][1] / d_places, 2)) + ' ' + str(round(grid_dim[breaklines_mst_uq[i1][i2]][2] / d_places, 2)) + ' ' + str(R1) + ' ' + str(G1) + ' ' + str(B1) + '\n')
            f4.write('v ' + str(round((grid_dim[breaklines_mst_uq[i1][i2]][xyz_pos[0]] / d_places) - xyz_return[xyz_pos[0]], 2)) + ' ' + str(round((grid_dim[breaklines_mst_uq[i1][i2]][xyz_pos[1]] / d_places) - xyz_return[xyz_pos[1]], 2)) + ' ' + str(round((grid_dim[breaklines_mst_uq[i1][i2]][xyz_pos[2]] / d_places) - xyz_return[xyz_pos[2]], 2)) + ' ' + str(R1) + ' ' + str(G1) + ' ' + str(B1) + '\n')
    
    f4.write('\ng\n')
    for i1 in range(len(breaklines_mst)): #len(breaklines_mst)
        f4.write('# ' + str(i1 + 1) + '\n')
        for i2 in range(len(breaklines_mst[i1])):
            temp1 = 0
            temp2 = 0
            for k in range(len(breaklines_mst_uq[i1])):
                if breaklines_mst_uq[i1][k] == breaklines_mst[i1][i2][0]:
                    temp1 = k
                    break
            for k in range(len(breaklines_mst_uq[i1])):
                if breaklines_mst_uq[i1][k] == breaklines_mst[i1][i2][1]:
                    temp2 = k
                    break
            temp1 = temp1 + breaklines_uq_pos[i1][0]
            temp2 = temp2 + breaklines_uq_pos[i1][0]
            f4.write('l ' + str(temp1) + ' ' + str(temp2) + '\n')
    f4.close()

    os.remove(final_fname)
    #os.remove(temp_loc + 'csv_generated.csv')
    os.remove(temp_loc + 'csv_modified.csv')
    #print("Done")

    clear_variables()
    
    return 0

def take_second(elem):
    return elem[1]
def take_first(elem):
    return elem[0]

#if __name__ == '__main__':
#    multiprocessing.freeze_support()