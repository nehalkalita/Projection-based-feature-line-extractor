#import numpy as np
import math
#from numba import jit
import sys
import csv
#import threading
import multiprocessing
import os
#os.environ["OPENBLAS_MAIN_FREE"] = "1"
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ranges = [[], [], [], []] # Yi_range_l, Xi_range_l, Yi_range_r, Xi_range_r
#Yi_range_l = []
#Xi_range_l = []
#Yi_range_r = []
#Xi_range_r = []
X = []
Y = []
Z = []
Y_vals = []
X_vals = []
Grid_Y = []
max_blk_height_y_final = []
max_blk_height_x_final = []
min_blk_height_y_final = []
min_blk_height_x_final = []

def fill_X_Y_vals(coord, X_Y_s, XY_vals, X, Y, Z):
    if coord == 0:
        i = 0
        Y_len = len(Y)
        while (i < Y_len):
            Xi = round(float(X[i]))
            Xi = Xi - X_Y_s
            Xi = int(Xi)
            Yi = round(float(Y[i]))
            Zi = round(float(Z[i]))
            XY_vals[Xi].append([Xi + X_Y_s, int(Yi), int(Zi)])
            i = i + 1

        i1 = 0
        while (i1 < len(XY_vals)):
            XY_vals[i1].sort(key = take_second)    
            i1 = i1 + 1
        return coord, XY_vals
    else:
        i = 0
        X_len = len(X)
        while (i < X_len):
            Yi = round(float(Y[i]))
            Yi = Yi - X_Y_s
            Yi = int(Yi)
            Xi = round(float(X[i]))
            Zi = round(float(Z[i]))
            XY_vals[Yi].append([int(Xi), Yi + X_Y_s, int(Zi)])
            i = i + 1

        i1 = 0
        while (i1 < len(XY_vals)):
            XY_vals[i1].sort(key = take_first)
            i1 = i1 + 1
        return coord, XY_vals

def get_X_Y_vals(coord):
    if coord[0] == 0:
        global X_vals
        X_vals = coord[1]
    else:
        global Y_vals
        Y_vals = coord[1]
            
def Y_X_range(i, dim, Ymax, Xmax):
    ranges_i = []
    if i == 0 or i == 2:
        Yi = 0
        while (Yi * dim < Ymax):
            ranges_i.append(-1)
            Yi = Yi + 1
    else:
        Xi = 0
        while (Xi * dim < Xmax):
            ranges_i.append(-1)
            Xi = Xi + 1
    #print(i, len(ranges_i))
    return i, ranges_i

def Y_X_range_2(i, dim, Ymax, Xmax):
    ranges_i = [[], []]
    if i == 0:
        Yi = 0
        while (Yi * dim < Ymax):
            ranges_i[0].append(-1)
            ranges_i[1].append(-1)
            Yi = Yi + 1
    else:
        Xi = 0
        while (Xi * dim < Xmax):
            ranges_i[0].append(-1)
            ranges_i[1].append(-1)
            Xi = Xi + 1
    #print(i, len(ranges_i))
    return i, ranges_i

def get_range(ranges_i):
    global ranges
    ranges[ranges_i[0]] = ranges_i[1]
    
def get_range_2(ranges_i):
    global ranges
    ranges[ranges_i[0]] = ranges_i[1][0]
    ranges[ranges_i[0] + 2] = ranges_i[1][1]
    
def Y_range_0(dim, Xmax, Ymax, Xs, Y_vals, range_i):
    # increment Y_pos and X_pos till dim_range = max position of points in X_vals and Y_vals
    Yi = 0
    while (Yi * dim < Ymax):
        flag1 = 0 # 1 if value found for Yi/Xi ranges
        Xi = 0
        while ((Xi * dim < Xmax) and (flag1 == 0)):
            #Grid_Y = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * Y_pos
            while ((dim_range < dim * (Y_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Ymax:
                    while ((i < len(Y_vals[dim_range])) and (flag1 == 0)):
                        if (Y_vals[dim_range][i][0] >= Xs + (dim * X_pos) and Y_vals[dim_range][i][0] < Xs + (dim * (X_pos + 1))):
                            #Grid_Y[0].append([Y_vals[dim_range][i][0], Y_vals[dim_range][i][1], Y_vals[dim_range][i][2]])
                            flag1 = 1
                            range_i[Yi] = dim * X_pos
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Xi = Xi + 1
        Yi = Yi + 1
    return 0, range_i

def Y_range_1(dim, Xmax, Ymax, Xs, Y_vals, range_i):
    # increment Y_pos and X_pos till dim_range = max position of points in X_vals and Y_vals
    Yi = 0
    while (Yi * dim < Ymax):
        flag1 = 0
        Xi = math.ceil(Xmax / dim) # int(Xmax / dim)
        temp1 = Xi
        if int(Xmax / dim) != Xi:
            Xi_f = Xi - (Xmax / dim) # fractional
        else:
            Xi_f = Xi
        while ((Xi * dim >= 0) and (flag1 == 0)):
            #Grid_Y = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * Y_pos
            while ((dim_range < dim * (Y_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Ymax:
                    while ((i < len(Y_vals[dim_range])) and (flag1 == 0)):
                        if (Y_vals[dim_range][i][0] < Xs + (dim * X_pos) and Y_vals[dim_range][i][0] >= Xs + (dim * (X_pos - 1))):
                            #Grid_Y[0].append([Y_vals[dim_range][i][0], Y_vals[dim_range][i][1], Y_vals[dim_range][i][2]])
                            flag1 = 1
                            if Xi == temp1:
                                range_i[Yi] = (dim * X_pos) - int(dim * Xi_f)
                            else:
                                range_i[Yi] = dim * X_pos
                            #range_i[Yi] = Y_vals[dim_range][i][0]
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Xi = Xi - 1            
        Yi = Yi + 1
    return 2, range_i

def X_range_0(dim, Xmax, Ymax, Ys, X_vals, range_i):
    Xi = 0
    while (Xi * dim < Xmax):
        flag1 = 0 # 1 if value found for Yi/Xi ranges
        Yi = 0
        while ((Yi * dim < Ymax) and (flag1 == 0)):
            #Grid_X = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * X_pos
            while ((dim_range < dim * (X_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Xmax:
                    while ((i < len(X_vals[dim_range])) and (flag1 == 0)):
                        if (X_vals[dim_range][i][1] >= Ys + (dim * Y_pos) and X_vals[dim_range][i][1] < Ys + (dim * (Y_pos + 1))):
                            #Grid_X[0].append([X_vals[dim_range][i][0], X_vals[dim_range][i][1], X_vals[dim_range][i][2]])
                            flag1 = 1
                            range_i[Xi] = dim * Y_pos
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Yi = Yi + 1
        Xi = Xi + 1
    return 1, range_i

def X_range_1(dim, Xmax, Ymax, Ys, X_vals, range_i):
    Xi = 0
    while (Xi * dim < Xmax):        
        flag1 = 0
        Yi = math.ceil(Ymax / dim) # int(Ymax / dim)
        temp1 = Yi
        if int(Ymax / dim) != Yi:
            Yi_f = Yi - (Ymax / dim) # fractional
        else:
            Yi_f = Yi
        while ((Yi * dim >= 0) and (flag1 == 0)):
            #Grid_X = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * X_pos
            while ((dim_range < dim * (X_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Xmax:
                    while ((i < len(X_vals[dim_range])) and (flag1 == 0)):
                        if (X_vals[dim_range][i][1] < Ys + (dim * Y_pos) and X_vals[dim_range][i][1] >= Ys + (dim * (Y_pos - 1))):
                            #Grid_X[0].append([X_vals[dim_range][i][0], X_vals[dim_range][i][1], X_vals[dim_range][i][2]])
                            flag1 = 1
                            if Yi == temp1:
                                range_i[Xi] = (dim * Y_pos) - int(dim * Yi_f)
                            else:
                                range_i[Xi] = dim * Y_pos
                            #range_i[Xi] = X_vals[dim_range][i][1]
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Yi = Yi - 1
        Xi = Xi + 1
    return 3, range_i

def Y_range_lr(dim, Xmax, Ymax, Xs, Y_vals, range_l, range_r):
    # increment Y_pos and X_pos till dim_range = max position of points in X_vals and Y_vals
    Yi = 0
    while (Yi * dim < Ymax):
        flag1 = 0 # 1 if value found for Yi/Xi ranges
        Xi = 0
        while ((Xi * dim < Xmax) and (flag1 == 0)):
            #Grid_Y = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * Y_pos
            while ((dim_range < dim * (Y_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Ymax:
                    while ((i < len(Y_vals[dim_range])) and (flag1 == 0)):
                        if (Y_vals[dim_range][i][0] >= Xs + (dim * X_pos) and Y_vals[dim_range][i][0] < Xs + (dim * (X_pos + 1))):
                            #Grid_Y[0].append([Y_vals[dim_range][i][0], Y_vals[dim_range][i][1], Y_vals[dim_range][i][2]])
                            flag1 = 1
                            range_l[Yi] = dim * X_pos
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Xi = Xi + 1
        Yi = Yi + 1
    
    Yi = 0
    while (Yi * dim < Ymax):
        flag1 = 0
        Xi = math.ceil(Xmax / dim) # int(Xmax / dim)
        temp1 = Xi
        if int(Xmax / dim) != Xi:
            Xi_f = Xi - (Xmax / dim) # fractional
        else:
            Xi_f = Xi
        while ((Xi * dim >= 0) and (flag1 == 0)):
            #Grid_Y = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * Y_pos
            while ((dim_range < dim * (Y_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Ymax:
                    while ((i < len(Y_vals[dim_range])) and (flag1 == 0)):
                        if (Y_vals[dim_range][i][0] < Xs + (dim * X_pos) and Y_vals[dim_range][i][0] >= Xs + (dim * (X_pos - 1))):
                            #Grid_Y[0].append([Y_vals[dim_range][i][0], Y_vals[dim_range][i][1], Y_vals[dim_range][i][2]])
                            flag1 = 1
                            if Xi == temp1:
                                range_r[Yi] = (dim * X_pos) - int(dim * Xi_f)
                            else:
                                range_r[Yi] = dim * X_pos
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Xi = Xi - 1            
        Yi = Yi + 1
    return 0, 2, range_l, range_r

def X_range_lr(dim, Xmax, Ymax, Ys, X_vals, range_l, range_r):
    Xi = 0
    while (Xi * dim < Xmax):
        flag1 = 0 # 1 if value found for Yi/Xi ranges
        Yi = 0
        while ((Yi * dim < Ymax) and (flag1 == 0)):
            #Grid_X = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * X_pos
            while ((dim_range < dim * (X_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Xmax:
                    while ((i < len(X_vals[dim_range])) and (flag1 == 0)):
                        if (X_vals[dim_range][i][1] >= Ys + (dim * Y_pos) and X_vals[dim_range][i][1] < Ys + (dim * (Y_pos + 1))):
                            #Grid_X[0].append([X_vals[dim_range][i][0], X_vals[dim_range][i][1], X_vals[dim_range][i][2]])
                            flag1 = 1
                            range_l[Xi] = dim * Y_pos
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Yi = Yi + 1
        Xi = Xi + 1
    
    Xi = 0
    while (Xi * dim < Xmax):        
        flag1 = 0
        Yi = math.ceil(Ymax / dim) # int(Ymax / dim)
        temp1 = Yi
        if int(Ymax / dim) != Yi:
            Yi_f = Yi - (Ymax / dim) # fractional
        else:
            Yi_f = Yi
        while ((Yi * dim >= 0) and (flag1 == 0)):
            #Grid_X = [[]]
            Y_pos = Yi
            X_pos = Xi
            
            dim_range = dim * X_pos
            while ((dim_range < dim * (X_pos + 1)) and (flag1 == 0)):
                i = 0
                if dim_range < Xmax:
                    while ((i < len(X_vals[dim_range])) and (flag1 == 0)):
                        if (X_vals[dim_range][i][1] < Ys + (dim * Y_pos) and X_vals[dim_range][i][1] >= Ys + (dim * (Y_pos - 1))):
                            #Grid_X[0].append([X_vals[dim_range][i][0], X_vals[dim_range][i][1], X_vals[dim_range][i][2]])
                            flag1 = 1
                            if Yi == temp1:
                                range_r[Xi] = (dim * Y_pos) - int(dim * Yi_f)
                            else:
                                range_r[Xi] = dim * Y_pos
                        i = i + 1
                else:
                    break
                dim_range = dim_range + 1
            Yi = Yi - 1
        Xi = Xi + 1
    return 1, 3, range_l, range_r

def get_range_i(range_i):
    global ranges
    ranges[range_i[0]] = range_i[1]

def get_range_2_i(range_i):
    global ranges
    ranges[range_i[0]] = range_i[2]
    ranges[range_i[1]] = range_i[3]

def detect_thickness(axis_XY, dim, blk_span_r, blk_span_v, len_X_dim, len_Y_dim, range_l, range_r, j1, j2, XY_line_avg, XY_line_index, min_local_height, median_covg_perc):
    #axis_XY = 1 -> X
    median_covg_units = 0
    max_blk_height_xy = []
    min_blk_height_xy = []
    i1 = j1
    while (i1 <= j2):
        max_blk_height_xy.append([])
        if i1 <= len(range_l) - 1:
            i = int(range_l[i1] / dim)
            while (i < range_r[i1] / dim):
                temp2 = [0,0]
                if axis_XY == 0:
                    if i + dim < len_Y_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_Y_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                else:
                    if i + dim < len_X_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_X_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2

                temp1 = 0
                j = i
                while (j < i2):
                    if XY_line_avg[i1 - j1][j][2] == 1:
                        blk_height = [XY_line_avg[i1 - j1][j][3], XY_line_index[i1 - j1][j], j]
                        temp1 = 1
                        break
                    j = j + 1
                while (j < i2):
                    if XY_line_avg[i1 - j1][j][2] == 1 and XY_line_avg[i1 - j1][j][3] >= blk_height[0]:
                        blk_height[0] = XY_line_avg[i1 - j1][j][3]
                        blk_height[1] = XY_line_index[i1 - j1][j]
                        blk_height[2] = j
                    j = j + 1
                
                min_local_xy = blk_height[0] # used to store local minimum of section for comparing and filtering
                j = i 
                while (j < i2):
                    if XY_line_avg[i1 - j1][j][2] == 1 and XY_line_avg[i1 - j1][j][3] <= blk_height[0]:
                        min_local_xy = XY_line_avg[i1 - j1][j][3]
                    j = j + 1
                if abs(blk_height[0] - min_local_xy) >= min_local_height:
                    flag1 = 0
                    if temp2[0] == 1:
                        if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + median_covg_units)):
                            flag1 = 1
                    else:
                        if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - 0.5 - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + 0.5 + median_covg_units)):
                            flag1 = 1
                    if flag1 == 1:
                        # don't add in max_blk_height if span touches boundary
                        if temp1 == 1: # need to check limits as per values in 'ranges'
                            if (blk_height[2] - blk_span_r) > i and (blk_height[2] + blk_span_r) < i2 - 1:
                                if max_blk_height_xy[-1].__contains__(blk_height[1]) == False:
                                    max_blk_height_xy[-1].append(blk_height[1]) # [blk_height[0], blk_height[1]]
                i = i + 1

            min_blk_height_xy.append([])
            i = int(range_l[i1] / dim)
            while (i < range_r[i1] / dim):
                temp2 = [0,0]
                if axis_XY == 0:
                    if i + dim < len_Y_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_Y_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                else:
                    if i + dim < len_X_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_X_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                temp1 = 0    
                j = i
                while (j < i2):
                    if XY_line_avg[i1 - j1][j][2] == 1:
                        blk_height = [XY_line_avg[i1 - j1][j][3], XY_line_index[i1 - j1][j], j]
                        temp1 = 1
                        break
                    j = j + 1
                while (j < i2):
                    if XY_line_avg[i1 - j1][j][2] == 1 and XY_line_avg[i1 - j1][j][3] <= blk_height[0]:
                        blk_height[0] = XY_line_avg[i1 - j1][j][3]
                        blk_height[1] = XY_line_index[i1 - j1][j]
                        blk_height[2] = j
                    j = j + 1
                
                max_local_xy = blk_height[0] # used to store local maximum of section for comparing and filtering
                j = i
                while (j < i2):
                    if XY_line_avg[i1 - j1][j][2] == 1 and XY_line_avg[i1 - j1][j][3] >= blk_height[0]:
                        max_local_xy = XY_line_avg[i1 - j1][j][3]
                    j = j + 1
                if abs(max_local_xy - blk_height[0]) >= min_local_height:
                    flag1 = 0
                    if temp2[0] == 1:
                        if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + median_covg_units)):
                            flag1 = 1
                    else:
                        if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - 0.5 - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + 0.5 + median_covg_units)):
                            flag1 = 1
                    if flag1 == 1:
                        # don't add in min_blk_height if span touches boundary
                        if temp1 == 1: # need to check limits as per values in 'ranges'
                            if (blk_height[2] - blk_span_v) > i and (blk_height[2] + blk_span_v) < i2 - 1:
                                if min_blk_height_xy[-1].__contains__(blk_height[1]) == False:
                                    min_blk_height_xy[-1].append(blk_height[1]) # [blk_height[0], blk_height[1]]
                
                i = i + 1    
        
        else:
            min_blk_height_xy.append([])
        i1 = i1 + 1
       
    return j1, j2, blk_span_r, blk_span_v, len_X_dim, len_Y_dim, max_blk_height_xy, min_blk_height_xy

def get_thickness_y(result_y):
    global Grid_Y
    global max_blk_height_y_final
    global min_blk_height_y_final
    
    i1 = result_y[0]
    while (i1 <= result_y[1]):
        for i in result_y[6][i1 - result_y[0]]:
            j = 0
            while (j < len(Grid_Y[i])):
                if Grid_Y[i][j][5] == 0 and Grid_Y[i][j][6] == 169 and Grid_Y[i][j][7] == 51:
                    Grid_Y[i][j][5] = 255
                    Grid_Y[i][j][6] = 191
                    Grid_Y[i][j][7] = 0
                else:
                    Grid_Y[i][j][5] = 255
                    Grid_Y[i][j][6] = 0
                    Grid_Y[i][j][7] = 0
                j = j + 1
            
            i2 = -1
            while(i2 >= 0 - result_y[2]):
                temp1 = i + (i2 * math.ceil(result_y[4]))
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 0
                            Grid_Y[temp1][j][7] = 0
                        j = j + 1
                i2 = i2 - 1
            
            i2 = 1
            while(i2 <= result_y[2]):
                temp1 = i + (i2 * math.ceil(result_y[4]))
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 0
                            Grid_Y[temp1][j][7] = 0
                        j = j + 1
                i2 = i2 + 1
        
        for i in result_y[7][i1 - result_y[0]]:
            j = 0
            while (j < len(Grid_Y[i])):
                if Grid_Y[i][j][5] == 255 and Grid_Y[i][j][6] == 0 and Grid_Y[i][j][7] == 0:
                    Grid_Y[i][j][5] = 255
                    Grid_Y[i][j][6] = 191
                    Grid_Y[i][j][7] = 0
                else:
                    Grid_Y[i][j][5] = 0
                    Grid_Y[i][j][6] = 169
                    Grid_Y[i][j][7] = 51
                j = j + 1
            
            i2 = -1
            while(i2 >= 0 - result_y[3]):
                temp1 = i + (i2 * math.ceil(result_y[4]))
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 0
                            Grid_Y[temp1][j][6] = 169
                            Grid_Y[temp1][j][7] = 51
                        j = j + 1
                i2 = i2 - 1
            
            i2 = 1
            while(i2 <= result_y[3]):
                temp1 = i + (i2 * math.ceil(result_y[4]))
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 0
                            Grid_Y[temp1][j][6] = 169
                            Grid_Y[temp1][j][7] = 51
                        j = j + 1
                i2 = i2 + 1        
        
        max_blk_height_y_final[i1] = result_y[6][i1 - result_y[0]]
        min_blk_height_y_final[i1] = result_y[7][i1 - result_y[0]]
        i1 = i1 + 1

def get_thickness_x(result_x):
    global Grid_Y
    global max_blk_height_x_final
    global min_blk_height_x_final
    
    i1 = result_x[0]
    while (i1 <= result_x[1]):
        for i in result_x[6][i1 - result_x[0]]:
            j = 0
            while (j < len(Grid_Y[i])):
                if Grid_Y[i][j][5] == 0 and Grid_Y[i][j][6] == 169 and Grid_Y[i][j][7] == 51:
                    Grid_Y[i][j][5] = 255
                    Grid_Y[i][j][6] = 191
                    Grid_Y[i][j][7] = 0
                else:
                    Grid_Y[i][j][5] = 255
                    Grid_Y[i][j][6] = 0
                    Grid_Y[i][j][7] = 0
                j = j + 1
            
            i2 = -1
            while(i2 >= 0 - result_x[2]):
                temp1 = i + i2
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 0
                            Grid_Y[temp1][j][7] = 0
                        j = j + 1
                i2 = i2 - 1
            
            i2 = 1
            while(i2 <= result_x[2]):
                temp1 = i + i2
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 0
                            Grid_Y[temp1][j][7] = 0
                        j = j + 1
                i2 = i2 + 1
        
        for i in result_x[7][i1 - result_x[0]]:
            j = 0
            while (j < len(Grid_Y[i])):
                if Grid_Y[i][j][5] == 255 and Grid_Y[i][j][6] == 0 and Grid_Y[i][j][7] == 0:
                    Grid_Y[i][j][5] = 255
                    Grid_Y[i][j][6] = 191
                    Grid_Y[i][j][7] = 0
                else:
                    Grid_Y[i][j][5] = 0
                    Grid_Y[i][j][6] = 169
                    Grid_Y[i][j][7] = 51
                j = j + 1
            
            i2 = -1
            while(i2 >= 0 - result_x[3]):
                temp1 = i + i2
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 0
                            Grid_Y[temp1][j][6] = 169
                            Grid_Y[temp1][j][7] = 51
                        j = j + 1
                i2 = i2 - 1
            
            i2 = 1
            while(i2 <= result_x[3]):
                temp1 = i + i2
                if Grid_Y[temp1] != []:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                            Grid_Y[temp1][j][5] = 255
                            Grid_Y[temp1][j][6] = 191
                            Grid_Y[temp1][j][7] = 0
                        else:
                            Grid_Y[temp1][j][5] = 0
                            Grid_Y[temp1][j][6] = 169
                            Grid_Y[temp1][j][7] = 51
                        j = j + 1
                i2 = i2 + 1
        
        max_blk_height_x_final[i1] = result_x[6][i1 - result_x[0]]
        min_blk_height_x_final[i1] = result_x[7][i1 - result_x[0]]
        i1 = i1 + 1
    
def clear_variables():
    global ranges
    global X, Y, Z
    global Y_vals, X_vals
    global Grid_Y
    global max_blk_height_x_final, min_blk_height_x_final, max_blk_height_y_final, min_blk_height_y_final
    
    ranges = [[], [], [], []]
    X = []
    Y = []
    Z = []
    Y_vals = []
    X_vals = []
    Grid_Y = []
    max_blk_height_y_final = []
    max_blk_height_x_final = []
    min_blk_height_y_final = []
    min_blk_height_x_final = []

#@jit
def spatial_test(total_cores, temp_loc, dim, blk_sp, d_places, min_local_height, median_covg_perc):
    XYZC = open(temp_loc + 'csv_modified.csv', 'r')
    limits = open(resource_path('Limits.csv'), 'r')
    #f1 = open('C:/Users/Student/Documents/python/.vscode/Grid_final.txt', 'w')   # format: y_x
    blk_span_r = blk_sp
    blk_span_v = blk_sp
    # 5 to 7 (30 / 2 = 15; 15 / 2 = 7.5)
    temp_cores = total_cores
    if int(temp_cores) > total_cores:
        total_cores = total_cores + 0
    else:
        total_cores = int(temp_cores)
        
    final_fname = temp_loc + 'F'
    fname = ''
    fname = fname + '_' + str(dim) + '_' + str(blk_span_r)
    
    fname = fname + '.csv'
    final_fname = final_fname + fname
    f1 = open(final_fname, 'w', newline='')   # format: y_x
    f2 = open(resource_path('grid_n_decimal.csv'), 'w', newline='') # dim, Xi, Yi
    r1 = csv.reader(XYZC)
    r2 = csv.reader(limits)
    csv_write = csv.writer(f1, delimiter = ',')
    csv_write_dim = csv.writer(f2, delimiter = ',')
        
    dim = int(dim)
    blk_span_r = int(blk_span_r)
    blk_span_v = int(blk_span_v)
    
    d_places = int(d_places)
    temp1 = math.pow(10, d_places)
    Xs, Xl, Ys, Yl, Zs, Zl, Xmax, Ymax = 0, 0, 0, 0, 0, 0, 0, 0
    for line in r2:
        Xs = float(line[0]) * temp1   #since there are n digits after decimal
        Xl = float(line[1]) * temp1
        Ys = float(line[2]) * temp1
        Yl = float(line[3]) * temp1
        Zs = float(line[4]) * temp1
        Zl = float(line[5]) * temp1
        Xmax = int(float(line[6]))
        Ymax = int(float(line[7]))


    Xs = int(Xs)
    Xl = int(Xl)
    Ys = int(Ys)
    Yl = int(Yl)
    Zs = int(Zs)
    Zl = int(Zl)
    
    #blk_span_r: point spread function;   height_diff: depth of field
    #blk_span_r = 4
    
    #dim = 33
    
    #print(Xs, Xl, X, Xmax)
    #337104.57 337408.41 303.8399999999674 30384.0

    #print(Ys, Yl, Y, Ymax)
    #3817297.79 3817550.18 252.39000000013039 25239.0

    #print(Zs, Zl, Z, Zmax)
    #344.6 467.57 122.96999999999997 12297.0
    
    #print(Xs, Xl, X, Xmax)
    #337071.33 337671.54 600.2099999999627 60021.0

    #print(Ys, Yl, Y, Ymax)
    #3817083.34 3817723.32 639.9799999999814 63998.0

    #print(Zs, Zl, Z, Zmax)
    #306.33 573.71 267.38000000000005 26738.0
    
    global Y_vals
    global X_vals
    Y_vals = []
    X_vals = []
    global X
    global Y
    global Z
    X = []
    Y = []
    Z = []
    
    i = 0 
    while (i <= Ymax): #25239 63998
        Y_vals.append([])
        i = i + 1
    
    i = 0
    while (i <= Xmax):
        X_vals.append([])
        i = i + 1
    
    for line in r1:
        X.append(line[0])   #0
        Y.append(line[1])   #1
        Z.append(line[2])   #2
    
    if total_cores > 1 and len(X) > 2000000:
        p = multiprocessing.Pool(2)
        for i in range(2):
            if i == 0:
                p.apply_async(fill_X_Y_vals, args=(i, Xs, X_vals, X, Y, Z), callback=get_X_Y_vals)
            else:
                p.apply_async(fill_X_Y_vals, args=(i, Ys, Y_vals, X, Y, Z), callback=get_X_Y_vals)
        p.close()
        p.join()
        del p
        #for i in range(5):
        #    print('x:', X_vals[i][0], X_vals[i][1], X_vals[i][2], X_vals[i][3])
        #for i in range(5):
        #    print('y:', Y_vals[i][0], Y_vals[i][1], Y_vals[i][2], Y_vals[i][3])
    
    else:
        i = 0
        X_len = len(X)
        while (i < X_len):
            Yi = round(float(Y[i]))
            Yi = Yi - Ys #381729779 #381729779(small) 381708334(large)
            Yi = int(Yi)
            Xi = round(float(X[i]))
            Zi = round(float(Z[i]))
            #Y_vals[Yi].append([int(Xi), Yi + 381729779, int(Zi)])
            Y_vals[Yi].append([int(Xi), Yi + Ys, int(Zi)])
            
            i = i + 1

        i1 = 0
        while (i1 < len(Y_vals)):
            Y_vals[i1].sort(key = take_first)
            i1 = i1 + 1
            

        i = 0
        Y_len = len(Y)
        while (i < Y_len):
            Xi = round(float(X[i]))
            Xi = Xi - Xs # 33710457
            Xi = int(Xi)
            Yi = round(float(Y[i]))
            Zi = round(float(Z[i]))
            #Y_vals[Yi].append([int(Xi), Yi + 381729779, int(Zi)])
            X_vals[Xi].append([Xi + Xs, int(Yi), int(Zi)])
            i = i + 1

        i1 = 0
        while (i1 < len(X_vals)):
            X_vals[i1].sort(key = take_second)
            i1 = i1 + 1
    
    X.clear()
    Y.clear()
    Z.clear()
    
    #Xmax, Ymax = 400000000, 400000000 # only for testing
    #thread1 = threading.Thread(target=Y_X_range_init, args=(1, dim, Ymax))
    global ranges
    if total_cores > 3 and (Xmax >= 2000000 or Ymax >= 2000000):
        p = multiprocessing.Pool(4)
        for i in range(4):
            #result = p.map(Y_X_range, ranges, dim, Ymax, Xmax)
            p.apply_async(Y_X_range, args=(i, dim, Ymax, Xmax), callback=get_range)
        p.close()
        p.join()
        del p
    
    elif total_cores == 2 and (Xmax >= 2000000 or Ymax >= 2000000):
        p = multiprocessing.Pool(2)
        for i in range(2):
            p.apply_async(Y_X_range_2, args=(i, dim, Ymax, Xmax), callback=get_range_2)
        p.close()
        p.join()
        del p
    
    elif total_cores == 1 or total_cores > 1:
        Xi = 0
        while (Xi * dim < Xmax):
            #ranges[1] += [-1]
            ranges[1].append(-1)
            ranges[3].append(-1)
            Xi = Xi + 1
        Yi = 0
        while (Yi * dim < Ymax):
            ranges[0].append(-1)
            ranges[2].append(-1)
            Yi = Yi + 1
                    
    # find ranges for each lines horzonttally and vertically
    #Yi_range_l = []
    #Xi_range_l = []
    #Yi_range_r = []
    #Xi_range_r = []
    if total_cores > 3 and (Xmax >= 20000 or Ymax >= 20000):
        p = multiprocessing.Pool(4)
        for i in range(4):
            if i == 0:
                p.apply_async(Y_range_0, args=(dim, Xmax, Ymax, Xs, Y_vals, ranges[0]), callback=get_range_i)
            elif i == 1:
                p.apply_async(X_range_0, args=(dim, Xmax, Ymax, Ys, X_vals, ranges[1]), callback=get_range_i)
            elif i == 2:
                p.apply_async(Y_range_1, args=(dim, Xmax, Ymax, Xs, Y_vals, ranges[2]), callback=get_range_i)
            else:
                p.apply_async(X_range_1, args=(dim, Xmax, Ymax, Ys, X_vals, ranges[3]), callback=get_range_i)
        p.close()
        p.join()
        del p
        
    elif total_cores == 2 and (Xmax >= 20000 or Ymax >= 20000):
        p = multiprocessing.Pool(2)
        for i in range(2):
            if i == 0:
                p.apply_async(Y_range_lr, args=(dim, Xmax, Ymax, Xs, Y_vals, ranges[0], ranges[2]), callback=get_range_2_i)
            elif i == 1:
                p.apply_async(X_range_lr, args=(dim, Xmax, Ymax, Ys, X_vals, ranges[1], ranges[3]), callback=get_range_2_i)
        p.close()
        p.join()
        del p
        
    elif total_cores == 1 or total_cores > 1:
        # increment Y_pos and X_pos till dim_range = max position of points in X_vals and Y_vals
        Yi = 0
        while (Yi * dim < Ymax):
            flag1 = 0 # 1 if value found for Yi/Xi ranges
            Xi = 0
            while ((Xi * dim < Xmax) and (flag1 == 0)):
                #Grid_Y = [[]]
                Y_pos = Yi
                X_pos = Xi
                
                dim_range = dim * Y_pos
                while ((dim_range < dim * (Y_pos + 1)) and (flag1 == 0)):
                    i = 0
                    if dim_range < Ymax:
                        while ((i < len(Y_vals[dim_range])) and (flag1 == 0)):
                            if (Y_vals[dim_range][i][0] >= Xs + (dim * X_pos) and Y_vals[dim_range][i][0] < Xs + (dim * (X_pos + 1))):
                                #Grid_Y[0].append([Y_vals[dim_range][i][0], Y_vals[dim_range][i][1], Y_vals[dim_range][i][2]])
                                flag1 = 1
                                ranges[0][Yi] = dim * X_pos
                            i = i + 1
                    else:
                        break
                    dim_range = dim_range + 1
                Xi = Xi + 1
            Yi = Yi + 1
            
        Yi = 0
        while (Yi * dim < Ymax):
            flag1 = 0
            Xi = math.ceil(Xmax / dim) # int(Xmax / dim)
            temp1 = Xi
            if int(Xmax / dim) != Xi:
                Xi_f = Xi - (Xmax / dim) # fractional
            else:
                Xi_f = Xi
            while ((Xi * dim >= 0) and (flag1 == 0)):
                #Grid_Y = [[]]
                Y_pos = Yi
                X_pos = Xi
                
                dim_range = dim * Y_pos
                while ((dim_range < dim * (Y_pos + 1)) and (flag1 == 0)):
                    i = 0
                    if dim_range < Ymax:
                        while ((i < len(Y_vals[dim_range])) and (flag1 == 0)):
                            if (Y_vals[dim_range][i][0] < Xs + (dim * X_pos) and Y_vals[dim_range][i][0] >= Xs + (dim * (X_pos - 1))):
                                #Grid_Y[0].append([Y_vals[dim_range][i][0], Y_vals[dim_range][i][1], Y_vals[dim_range][i][2]])
                                flag1 = 1
                                if Xi == temp1:
                                    ranges[2][Yi] = (dim * X_pos) - int(dim * Xi_f)
                                else:
                                    ranges[2][Yi] = dim * X_pos
                            i = i + 1
                    else:
                        break
                    dim_range = dim_range + 1
                Xi = Xi - 1            
            Yi = Yi + 1
        
        Xi = 0
        while (Xi * dim < Xmax):
            flag1 = 0 # 1 if value found for Yi/Xi ranges
            Yi = 0
            while ((Yi * dim < Ymax) and (flag1 == 0)):
                #Grid_X = [[]]
                Y_pos = Yi
                X_pos = Xi
                
                dim_range = dim * X_pos
                while ((dim_range < dim * (X_pos + 1)) and (flag1 == 0)):
                    i = 0
                    if dim_range < Xmax:
                        while ((i < len(X_vals[dim_range])) and (flag1 == 0)):
                            if (X_vals[dim_range][i][1] >= Ys + (dim * Y_pos) and X_vals[dim_range][i][1] < Ys + (dim * (Y_pos + 1))):
                                #Grid_X[0].append([X_vals[dim_range][i][0], X_vals[dim_range][i][1], X_vals[dim_range][i][2]])
                                flag1 = 1
                                ranges[1][Xi] = dim * Y_pos
                            i = i + 1
                    else:
                        break
                    dim_range = dim_range + 1
                Yi = Yi + 1
            Xi = Xi + 1
        
        Xi = 0
        while (Xi * dim < Xmax):        
            flag1 = 0
            Yi = math.ceil(Ymax / dim) # int(Ymax / dim)
            temp1 = Yi
            if int(Ymax / dim) != Yi:
                Yi_f = Yi - (Ymax / dim) # fractional
            else:
                Yi_f = Yi
            while ((Yi * dim >= 0) and (flag1 == 0)):
                #Grid_X = [[]]
                Y_pos = Yi
                X_pos = Xi
                
                dim_range = dim * X_pos
                while ((dim_range < dim * (X_pos + 1)) and (flag1 == 0)):
                    i = 0
                    if dim_range < Xmax:
                        while ((i < len(X_vals[dim_range])) and (flag1 == 0)):
                            if (X_vals[dim_range][i][1] < Ys + (dim * Y_pos) and X_vals[dim_range][i][1] >= Ys + (dim * (Y_pos - 1))):
                                #Grid_X[0].append([X_vals[dim_range][i][0], X_vals[dim_range][i][1], X_vals[dim_range][i][2]])
                                flag1 = 1
                                if Yi == temp1:
                                    ranges[3][Xi] = (dim * Y_pos) - int(dim * Yi_f)
                                else:
                                    ranges[3][Xi] = dim * Y_pos
                            i = i + 1
                    else:
                        break
                    dim_range = dim_range + 1
                Yi = Yi - 1
            Xi = Xi + 1
    
    #for i in range(100):
        #print(i, [Xi_range_l[i], Xi_range_r[i]], [Yi_range_l[i], Yi_range_r[i]])
    #    print(i, [ranges[1][i], ranges[3][i]], [ranges[0][i], ranges[2][i]])
        # while loop
    
    global Grid_Y
    Grid_Y = []
    i = 0
    len_Y_dim = len(Y_vals) / dim
    len_X_dim = len(X_vals) / dim
    while (i < math.ceil(len_Y_dim) * math.ceil(len_X_dim)):
        Grid_Y.append([])
        i = i + 1
    
    res_range = 0
    X_range = 0
    Y_range = 0
    while (res_range < len(Y_vals)): # <= res means 1849 (=43*43) + 1 = 1850
        i = 0
        while (i < len(Y_vals[res_range])):
            X_range = Y_vals[res_range][i][0] - Xs
            X_range = int(X_range / dim)
            Y_range = Y_vals[res_range][i][1] - Ys
            Y_range = int(Y_range / dim)
            Grid_Y[(Y_range * math.ceil(len_X_dim)) + X_range].append([Y_vals[res_range][i][0], Y_vals[res_range][i][1], Y_vals[res_range][i][2], Y_range, X_range, 255, 255, 255])
            i = i + 1
        res_range = res_range + 1
    
    Y_vals = []
    X_vals = []
    
    Grid_avg = []
    i = 0
    while (i < len(Grid_Y)):
        Grid_avg.append([0,0,-1,0,-1,-1])
        i = i + 1
    
    i = 0
    while (i < len(Grid_Y)):
        if len(Grid_Y[i]) == 0:
            Grid_avg[i][0] = int(i / math.ceil(len_X_dim)) # Y
            Grid_avg[i][1] = i % math.ceil(len_X_dim) # X
        else:
            j = 0
            blk_height = 0
            while (j < len(Grid_Y[i])):
                blk_height = blk_height + Grid_Y[i][j][2]
                j = j + 1
            blk_height = blk_height / len(Grid_Y[i])
            Grid_avg[i][0] = int(i / math.ceil(len_X_dim))
            Grid_avg[i][1] = i % math.ceil(len_X_dim)
            Grid_avg[i][2] = 1
            Grid_avg[i][3] = blk_height
            Grid_avg[i][4] = Grid_Y[i][0][3]
            Grid_avg[i][5] = Grid_Y[i][0][4]
        i = i + 1
    
    
    # iterate through each horizontal and vertical line
    #total_cores = 1
    global max_blk_height_y_final
    global max_blk_height_x_final
    global min_blk_height_y_final
    global min_blk_height_x_final
    max_blk_height_y_final = []
    max_blk_height_x_final = []
    min_blk_height_y_final = []
    min_blk_height_x_final = []
    if total_cores > 1 and (Xmax >= 20000 or Ymax >= 20000):
        if math.ceil(len_X_dim) / total_cores >= 1:
            temp1_cores = total_cores
        else:
            temp1_cores = total_cores - 1
            while (temp1_cores >= 1):
                if math.ceil(len_X_dim) / temp1_cores >= 1:
                    break
                else:
                    temp1_cores = temp1_cores - 1
        p = multiprocessing.Pool(temp1_cores)
        for i in range(temp1_cores):
            Y_line_avg = []
            Y_line_index = []
            j1 = math.ceil(math.ceil(len_X_dim) / temp1_cores) * i
            j2 = math.ceil(math.ceil(len_X_dim) / temp1_cores) * (i + 1)
            i1 = j1
            while ((i1 < j2) and (i1 < len_X_dim)):
                max_blk_height_y_final.append([])
                min_blk_height_y_final.append([])
                Y_line_avg.append([])
                Y_line_index.append([])
                i2 = 0
                while (i2 < len_Y_dim):
                    temp1 = i1 + (i2 * math.ceil(len_X_dim))
                    Y_line_avg[-1].append(Grid_avg[temp1])
                    Y_line_index[-1].append(temp1)
                    i2 = i2 + 1
                i1 = i1 + 1
            p.apply_async(detect_thickness, args=(0, dim, blk_span_r, blk_span_v, len_X_dim, len_Y_dim, ranges[1], ranges[3], j1, i1 - 1, Y_line_avg, Y_line_index, min_local_height, median_covg_perc), callback=get_thickness_y)
            #p.apply_async(Y_range_0, args=(dim, Xmax, Ymax, Xs, Y_vals, ranges[0]), callback=get_range_i)
        p.close()
        p.join()
        del p
        
        if math.ceil(len_Y_dim) / total_cores >= 1:
            temp1_cores = total_cores
        else:
            temp1_cores = total_cores - 1
            while (temp1_cores >= 1):
                if math.ceil(len_X_dim) / temp1_cores >= 1:
                    break
                else:
                    temp1_cores = temp1_cores - 1
        p = multiprocessing.Pool(temp1_cores)
        for i in range(temp1_cores):
            X_line_avg = []
            X_line_index = []
            j1 = math.ceil(math.ceil(len_Y_dim) / temp1_cores) * i
            j2 = math.ceil(math.ceil(len_Y_dim) / temp1_cores) * (i + 1)
            i1 = j1
            while ((i1 < j2) and (i1 < len_Y_dim)):
                max_blk_height_x_final.append([])
                min_blk_height_x_final.append([])
                X_line_avg.append([])
                X_line_index.append([])
                i2 = 0
                while (i2 < len_X_dim):
                    temp1 = (i1 * math.ceil(len_X_dim)) + i2
                    X_line_avg[-1].append(Grid_avg[temp1])
                    X_line_index[-1].append(temp1)
                    i2 = i2 + 1
                i1 = i1 + 1
            p.apply_async(detect_thickness, args=(1, dim, blk_span_r, blk_span_v, len_X_dim, len_Y_dim, ranges[0], ranges[2], j1, i1 - 1, X_line_avg, X_line_index, min_local_height, median_covg_perc), callback=get_thickness_x)
        p.close()
        p.join()
        del p
    
    elif total_cores == 1 or total_cores > 1:
        i1 = 0
        while (i1 < len_X_dim):
            Y_line_avg = []
            Y_line_index = []
            i2 = 0
            while (i2 < len_Y_dim):
                temp1 = i1 + (i2 * math.ceil(len_X_dim))
                Y_line_avg.append(Grid_avg[temp1])
                Y_line_index.append(temp1)
                i2 = i2 + 1
                
            max_blk_height_y = [] # (y-position, x_of_Grid_Y-position)
            if i1 <= len(ranges[1]) - 1:
                i = int(ranges[1][i1] / dim) #0
                #while (i < len_Y_dim):   # identify block with max height in each section
                while (i < ranges[3][i1] / dim):   # identify block with max height in each section
                    temp2 = [0,0]
                    if i + dim < len_Y_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_Y_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                    temp1 = 0
                    j = i
                    while (j < i2):
                        if Y_line_avg[j][2] == 1:
                            blk_height = [Y_line_avg[j][3], Y_line_index[j], j]
                            temp1 = 1
                            break
                        j = j + 1
                    while (j < i2):
                        if Y_line_avg[j][2] == 1 and Y_line_avg[j][3] >= blk_height[0]:
                            blk_height[0] = Y_line_avg[j][3]
                            blk_height[1] = Y_line_index[j]
                            blk_height[2] = j
                        j = j + 1
                    
                    min_local_y = blk_height[0] # used to store local minimum of section for comparing and filtering
                    j = i 
                    while (j < i2):
                        if Y_line_avg[j][2] == 1 and Y_line_avg[j][3] <= blk_height[0]:
                            min_local_y = Y_line_avg[j][3]
                        j = j + 1
                    if abs(blk_height[0] - min_local_y) >= min_local_height:
                        flag1 = 0
                        if temp2[0] == 1:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + median_covg_units)):
                                flag1 = 1
                        else:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - 0.5 - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + 0.5 + median_covg_units)):
                                flag1 = 1
                        if flag1 == 1:
                            # don't add in max_blk_height if span touches boundary
                            if temp1 == 1: # need to check limits as per values in 'ranges'
                                if (blk_height[2] - blk_span_r) > i and (blk_height[2] + blk_span_r) < i2 - 1:
                                    if max_blk_height_y.__contains__(blk_height[1]) == False:
                                        max_blk_height_y.append(blk_height[1]) # [blk_height[0], blk_height[1]]
                    i = i + 1
                
                min_blk_height_y = [] # (y-position, x_of_Grid_Y-position)
                i = int(ranges[1][i1] / dim) #0
                #while (i < len_Y_dim):   # identify block with min height in each section
                while (i < ranges[3][i1] / dim):   # identify block with min height in each section
                    temp2 = [0,0]
                    if i + dim < len_Y_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_Y_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                    temp1 = 0
                    j = i
                    while (j < i2):
                        if Y_line_avg[j][2] == 1:
                            blk_height = [Y_line_avg[j][3], Y_line_index[j], j]
                            temp1 = 1
                            break
                        j = j + 1
                    while (j < i2):
                        if Y_line_avg[j][2] == 1 and Y_line_avg[j][3] <= blk_height[0]:
                            blk_height[0] = Y_line_avg[j][3]
                            blk_height[1] = Y_line_index[j]
                            blk_height[2] = j
                        j = j + 1
                    
                    max_local_y = blk_height[0] # used to store local maximum of section for comparing and filtering
                    j = i 
                    while (j < i2):
                        if Y_line_avg[j][2] == 1 and Y_line_avg[j][3] >= blk_height[0]:
                            max_local_y = Y_line_avg[j][3]
                        j = j + 1
                    if abs(max_local_y - blk_height[0]) >= min_local_height:
                        flag1 = 0
                        if temp2[0] == 1:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + median_covg_units)):
                                flag1 = 1
                        else:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - 0.5 - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + 0.5 + median_covg_units)):
                                flag1 = 1
                        if flag1 == 1:
                            # don't add in min_blk_height if span touches boundary
                            if temp1 == 1: # need to check limits as per values in 'ranges'
                                if (blk_height[2] - blk_span_v) > i and (blk_height[2] + blk_span_v) < i2 - 1:
                                    if min_blk_height_y.__contains__(blk_height[1]) == False:
                                        min_blk_height_y.append(blk_height[1]) # [blk_height[0], blk_height[1]]
                    i = i + 1

            else:
                min_blk_height_y = [] # (y-position, x_of_Grid_Y-position)
            max_blk_height_y_final.append(max_blk_height_y)
            min_blk_height_y_final.append(min_blk_height_y)
            
            for i in max_blk_height_y:
                j = 0
                while (j < len(Grid_Y[i])):
                    if Grid_Y[i][j][5] == 0 and Grid_Y[i][j][6] == 169 and Grid_Y[i][j][7] == 51:
                        Grid_Y[i][j][5] = 255
                        Grid_Y[i][j][6] = 191
                        Grid_Y[i][j][7] = 0
                    else:
                        Grid_Y[i][j][5] = 255
                        Grid_Y[i][j][6] = 0
                        Grid_Y[i][j][7] = 0
                    j = j + 1
                
                i2 = -1
                while(i2 >= 0 - blk_span_r):
                    temp1 = i + (i2 * math.ceil(len_X_dim))
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 0
                                Grid_Y[temp1][j][7] = 0
                            j = j + 1
                    i2 = i2 - 1
                
                i2 = 1
                while(i2 <= blk_span_r):
                    temp1 = i + (i2 * math.ceil(len_X_dim))
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 0
                                Grid_Y[temp1][j][7] = 0
                            j = j + 1
                    i2 = i2 + 1
            
            for i in min_blk_height_y:
                j = 0
                while (j < len(Grid_Y[i])):
                    if Grid_Y[i][j][5] == 255 and Grid_Y[i][j][6] == 0 and Grid_Y[i][j][7] == 0:
                        Grid_Y[i][j][5] = 255
                        Grid_Y[i][j][6] = 191
                        Grid_Y[i][j][7] = 0
                    else:
                        Grid_Y[i][j][5] = 0
                        Grid_Y[i][j][6] = 169
                        Grid_Y[i][j][7] = 51
                    j = j + 1
                
                i2 = -1
                while(i2 >= 0 - blk_span_v):
                    temp1 = i + (i2 * math.ceil(len_X_dim))
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 0
                                Grid_Y[temp1][j][6] = 169
                                Grid_Y[temp1][j][7] = 51
                            j = j + 1
                    i2 = i2 - 1
                
                i2 = 1
                while(i2 <= blk_span_v):
                    temp1 = i + (i2 * math.ceil(len_X_dim))
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 0
                                Grid_Y[temp1][j][6] = 169
                                Grid_Y[temp1][j][7] = 51
                            j = j + 1
                    i2 = i2 + 1
            
            #print(i1, len_X_dim)
            i1 = i1 + 1
        
        i1 = 0
        while (i1 < len_Y_dim):
            #X_line = []
            X_line_avg = []
            X_line_index = []
            i2 = 0
            while (i2 < len_X_dim):
                temp1 = (i1 * math.ceil(len_X_dim)) + i2
                #if Grid_Y[temp1] != []:
                #    Y_line.append([])
                #    j = 0
                #    while (j < len(Grid_Y[temp1])):
                #        Y_line[-1].append([Grid_Y[temp1][j][0], Grid_Y[temp1][j][1], Grid_Y[temp1][j][2], Grid_Y[temp1][j][3], Grid_Y[temp1][j][4]])
                #        j = j + 1
                X_line_avg.append(Grid_avg[temp1])
                X_line_index.append(temp1)
                #if i1 == 1:
                #    print(temp1, math.ceil(len_X_dim), math.ceil(len_Y_dim), len(Grid_Y))
                i2 = i2 + 1
                
            max_blk_height_x = [] # (y-position, x_of_Grid_Y-position)
            if i1 <= len(ranges[0]) - 1:
                i = int(ranges[0][i1] / dim) #0
                #while (i < len_X_dim):   # identify block with max height in each section
                while (i < ranges[2][i1] / dim):   # identify block with max height in each section
                    temp2 = [0,0]
                    if i + dim < len_X_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_X_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                    temp1 = 0
                    j = i
                    while (j < i2):
                        if X_line_avg[j][2] == 1:
                            blk_height = [X_line_avg[j][3], X_line_index[j], j]
                            temp1 = 1
                            break
                        j = j + 1
                    while (j < i2):
                        if X_line_avg[j][2] == 1 and X_line_avg[j][3] >= blk_height[0]:
                            blk_height[0] = X_line_avg[j][3]
                            blk_height[1] = X_line_index[j]
                            blk_height[2] = j
                        j = j + 1
                    
                    min_local_x = blk_height[0] # used to store local minimum of section for comparing and filtering
                    j = i 
                    while (j < i2):
                        if X_line_avg[j][2] == 1 and X_line_avg[j][3] <= blk_height[0]:
                            min_local_x = X_line_avg[j][3]
                        j = j + 1
                    if abs(blk_height[0] - min_local_x) >= min_local_height:
                        flag1 = 0
                        if temp2[0] == 1:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + median_covg_units)):
                                flag1 = 1
                        else:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - 0.5 - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + 0.5 + median_covg_units)):
                                flag1 = 1
                        if flag1 == 1:
                            # don't add in max_blk_height if span touches boundary
                            if temp1 == 1: # need to check limits as per values in 'ranges'
                                if (blk_height[2] - blk_span_r) > i and (blk_height[2] + blk_span_r) < i2 - 1:
                                    if max_blk_height_x.__contains__(blk_height[1]) == False:
                                        max_blk_height_x.append(blk_height[1]) # [blk_height[0], blk_height[1]]
                    i = i + 1
                
                min_blk_height_x = [] # (y-position, x_of_Grid_Y-position)
                i = int(ranges[0][i1] / dim) #0
                #while (i < len_X_dim):   # identify block with min height in each section
                while (i < ranges[2][i1] / dim):   # identify block with min height in each section
                    temp2 = [0,0]
                    if i + dim < len_X_dim:
                        i2 = i + dim
                        if dim % 2 == 0:
                            median_covg_units = ((dim / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = dim / 2
                        else:
                            median_covg_units = math.floor(dim / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = dim / 2
                    else:
                        i2 = math.ceil(len_X_dim) - 1 # i + (len_Y_dim - 1 - i)
                        if (i2 - i) % 2 == 0:
                            median_covg_units = (((i2 - i) / 2) - 0.5) * (median_covg_perc / 100)
                            temp2[1] = (i2 - i) / 2
                        else:
                            median_covg_units = math.floor((i2 - i) / 2) * (median_covg_perc / 100)
                            temp2[0] = 1 # odd number
                            temp2[1] = (i2 - i) / 2
                    temp1 = 0
                    j = i
                    while (j < i2):
                        if X_line_avg[j][2] == 1:
                            blk_height = [X_line_avg[j][3], X_line_index[j], j]
                            temp1 = 1
                            break
                        j = j + 1
                    while (j < i2):
                        if X_line_avg[j][2] == 1 and X_line_avg[j][3] <= blk_height[0]:
                            blk_height[0] = X_line_avg[j][3]
                            blk_height[1] = X_line_index[j]
                            blk_height[2] = j
                        j = j + 1
                    
                    max_local_x = blk_height[0] # used to store local maximum of section for comparing and filtering
                    j = i 
                    while (j < i2):
                        if X_line_avg[j][2] == 1 and X_line_avg[j][3] >= blk_height[0]:
                            max_local_x = X_line_avg[j][3]
                        j = j + 1
                    if abs(max_local_x - blk_height[0]) >= min_local_height:
                        flag1 = 0
                        if temp2[0] == 1:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + median_covg_units)):
                                flag1 = 1
                        else:
                            if ((blk_height[2] - i + 1) >= math.floor(temp2[1] - 0.5 - median_covg_units)) or ((i2 - blk_height[2]) <= math.ceil(temp2[1] + 0.5 + median_covg_units)):
                                flag1 = 1
                        if flag1 == 1:
                            # don't add in min_blk_height if span touches boundary
                            if temp1 == 1: # need to check limits as per values in 'ranges'
                                if (blk_height[2] - blk_span_v) > i and (blk_height[2] + blk_span_v) < i2 - 1:
                                    if min_blk_height_x.__contains__(blk_height[1]) == False:
                                        min_blk_height_x.append(blk_height[1]) # [blk_height[0], blk_height[1]]
                    i = i + 1
            
            else:
                min_blk_height_x = [] # (y-position, x_of_Grid_Y-position)    
            max_blk_height_x_final.append(max_blk_height_x)
            min_blk_height_x_final.append(min_blk_height_x)
            
            for i in max_blk_height_x:
                j = 0
                while (j < len(Grid_Y[i])):
                    if Grid_Y[i][j][5] == 0 and Grid_Y[i][j][6] == 169 and Grid_Y[i][j][7] == 51:
                        Grid_Y[i][j][5] = 255
                        Grid_Y[i][j][6] = 191
                        Grid_Y[i][j][7] = 0
                    else:
                        Grid_Y[i][j][5] = 255
                        Grid_Y[i][j][6] = 0
                        Grid_Y[i][j][7] = 0
                    j = j + 1
                
                i2 = -1
                while(i2 >= 0 - blk_span_r):
                    #temp1 = (i * math.ceil(len_X_dim)) + i2
                    temp1 = i + i2
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 0
                                Grid_Y[temp1][j][7] = 0
                            j = j + 1
                    i2 = i2 - 1
                
                i2 = 1
                while(i2 <= blk_span_r):
                    #temp1 = (i * math.ceil(len_X_dim)) + i2
                    temp1 = i + i2
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 0 and Grid_Y[temp1][j][6] == 169 and Grid_Y[temp1][j][7] == 51:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 0
                                Grid_Y[temp1][j][7] = 0
                            j = j + 1
                    i2 = i2 + 1
            
            for i in min_blk_height_x:
                j = 0
                while (j < len(Grid_Y[i])):
                    if Grid_Y[i][j][5] == 255 and Grid_Y[i][j][6] == 0 and Grid_Y[i][j][7] == 0:
                        Grid_Y[i][j][5] = 255
                        Grid_Y[i][j][6] = 191
                        Grid_Y[i][j][7] = 0
                    else:
                        Grid_Y[i][j][5] = 0
                        Grid_Y[i][j][6] = 169
                        Grid_Y[i][j][7] = 51
                    j = j + 1
                
                i2 = -1
                while(i2 >= 0 - blk_span_v):
                    #temp1 = (i * math.ceil(len_Y_dim)) + i2
                    temp1 = i + i2
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 0
                                Grid_Y[temp1][j][6] = 169
                                Grid_Y[temp1][j][7] = 51
                            j = j + 1
                    i2 = i2 - 1
                
                i2 = 1
                while(i2 <= blk_span_v):
                    #temp1 = (i * math.ceil(len_Y_dim)) + i2
                    temp1 = i + i2
                    if Grid_Y[temp1] != []:
                        j = 0
                        while (j < len(Grid_Y[temp1])):
                            if Grid_Y[temp1][j][5] == 255 and Grid_Y[temp1][j][6] == 0 and Grid_Y[temp1][j][7] == 0:
                                Grid_Y[temp1][j][5] = 255
                                Grid_Y[temp1][j][6] = 191
                                Grid_Y[temp1][j][7] = 0
                            else:
                                Grid_Y[temp1][j][5] = 0
                                Grid_Y[temp1][j][6] = 169
                                Grid_Y[temp1][j][7] = 51
                            j = j + 1
                    i2 = i2 + 1
            
            #print(i1, len_X_dim)
            i1 = i1 + 1
        
    # export dimension value and computed resolution of data
    csv_write_dim.writerow([str(dim), str(Xi), str(Yi), str(d_places)])
    
    i1 = 0
    while (i1 < len(max_blk_height_y_final)):
        i2 = 0
        while (i2 < len(max_blk_height_y_final[i1])):
            if Grid_Y[max_blk_height_y_final[i1][i2]] != []:
                temp1 = max_blk_height_y_final[i1][i2]
                if Grid_Y[temp1][0][6] != 169:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        csv_write.writerow([str(Grid_Y[temp1][j][0]), str(Grid_Y[temp1][j][1]), str(Grid_Y[temp1][j][2]), str(Grid_Y[temp1][j][5]), str(Grid_Y[temp1][j][6]), str(Grid_Y[temp1][j][7]), str(Grid_Y[temp1][j][3]), str(Grid_Y[temp1][j][4])])
                        j = j + 1
            i2 = i2 + 1
        i1 = i1 + 1
    i1 = 0
    while (i1 < len(max_blk_height_x_final)):
        i2 = 0
        while (i2 < len(max_blk_height_x_final[i1])):
            if Grid_Y[max_blk_height_x_final[i1][i2]] != []:
                temp1 = max_blk_height_x_final[i1][i2]
                if Grid_Y[temp1][0][6] != 169:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        csv_write.writerow([str(Grid_Y[temp1][j][0]), str(Grid_Y[temp1][j][1]), str(Grid_Y[temp1][j][2]), str(Grid_Y[temp1][j][5]), str(Grid_Y[temp1][j][6]), str(Grid_Y[temp1][j][7]), str(Grid_Y[temp1][j][3]), str(Grid_Y[temp1][j][4])])
                        j = j + 1
            i2 = i2 + 1
        i1 = i1 + 1
    i1 = 0
    while (i1 < len(min_blk_height_y_final)):
        i2 = 0
        while (i2 < len(min_blk_height_y_final[i1])):
            if Grid_Y[min_blk_height_y_final[i1][i2]] != []:
                temp1 = min_blk_height_y_final[i1][i2]
                if Grid_Y[temp1][0][6] != 0:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        csv_write.writerow([str(Grid_Y[temp1][j][0]), str(Grid_Y[temp1][j][1]), str(Grid_Y[temp1][j][2]), str(Grid_Y[temp1][j][5]), str(Grid_Y[temp1][j][6]), str(Grid_Y[temp1][j][7]), str(Grid_Y[temp1][j][3]), str(Grid_Y[temp1][j][4])])
                        j = j + 1
            i2 = i2 + 1
        i1 = i1 + 1
    i1 = 0
    while (i1 < len(min_blk_height_x_final)):
        i2 = 0
        while (i2 < len(min_blk_height_x_final[i1])):
            if Grid_Y[min_blk_height_x_final[i1][i2]] != []:
                temp1 = min_blk_height_x_final[i1][i2]
                if Grid_Y[temp1][0][6] != 0:
                    j = 0
                    while (j < len(Grid_Y[temp1])):
                        csv_write.writerow([str(Grid_Y[temp1][j][0]), str(Grid_Y[temp1][j][1]), str(Grid_Y[temp1][j][2]), str(Grid_Y[temp1][j][5]), str(Grid_Y[temp1][j][6]), str(Grid_Y[temp1][j][7]), str(Grid_Y[temp1][j][3]), str(Grid_Y[temp1][j][4])])
                        j = j + 1
            i2 = i2 + 1
        i1 = i1 + 1
    
    clear_variables()

    return 0

def take_second(elem):
    return elem[1]
def take_first(elem):
    return elem[0]

#if __name__ == '__main__':
#    multiprocessing.freeze_support()