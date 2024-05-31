import csv
import math
#import time
#import multiprocessing
import os
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

def gen_csv(location1, temp_loc, res, total_cores, en_x, en_y, en_z, r_skip):
    msg1 = 'Enter correct column numbers'
    if min(en_x, en_y, en_z) < 0:
        return msg1
    elif (en_x == en_y) or (en_x == en_z) or (en_y == en_z):
        return msg1
    
    vals = detect_dimension(res, total_cores, temp_loc, location1, en_x, en_y, en_z, r_skip)
    return vals[0], vals[1], vals[2]

def detect_dimension(res, total_cores, temp_loc, location1, en_x, en_y, en_z, r_skip):
    #global res
    XYZC1 = open(location1, 'r')
    XYZC2 = open(location1, 'r')
    r1 = csv.reader(XYZC1)
    r2 = csv.reader(XYZC2)
    
    Xl = 0
    Yl = 0
    Zl = 0
    #csv_cn = 0
    if r_skip == 0:
        for i in r1:
            try:
                Xi = float(i[en_x])
                Yi = float(i[en_y])
                Zi = float(i[en_z])
                if Xi > Xl:
                    Xl = Xi
                if Yi > Yl:
                    Yl = Yi
                if Zi > Zl:
                    Zl = Zi
            except:
                msg1 = 'Wrong column numbers / Defective data'
                return msg1
            #csv_cn = csv_cn + 1
    else:
        cn_skip = 0 # count skipped rows
        for i in r1:
            try:
                if cn_skip < r_skip:
                    cn_skip += 1
                else:
                    Xi = float(i[en_x])
                    Yi = float(i[en_y])
                    Zi = float(i[en_z])
                    if Xi > Xl:
                        Xl = Xi
                    if Yi > Yl:
                        Yl = Yi
                    if Zi > Zl:
                        Zl = Zi
            except:
                msg1 = 'Wrong column numbers / Defective data'
                return msg1
    XYZC1.close()

    Xs = Xl
    Ys = Yl
    Zs = Zl
    if r_skip == 0:
        for i in r2:
            try:
                Xi = float(i[en_x])
                Yi = float(i[en_y])
                Zi = float(i[en_z])
                if Xi < Xs:
                    Xs = Xi
                if Yi < Ys:
                    Ys = Yi
                if Zi < Zs:
                    Zs = Zi
            except:
                msg1 = 'Wrong column numbers / Defective data'
                return msg1
    else:
        cn_skip = 0 # count skipped rows
        for i in r2:
            try:
                if cn_skip < r_skip:
                    cn_skip += 1
                else:
                    Xi = float(i[en_x])
                    Yi = float(i[en_y])
                    Zi = float(i[en_z])
                    if Xi < Xs:
                        Xs = Xi
                    if Yi < Ys:
                        Ys = Yi
                    if Zi < Zs:
                        Zs = Zi
            except:
                msg1 = 'Wrong column numbers / Defective data'
                return msg1
            
    XYZC2.close()

    #res = 0.01
    res_i = int(res)
    Xs = round(Xs, res_i)
    Xl = round(Xl, res_i)
    Ys = round(Ys, res_i)
    Yl = round(Yl, res_i)
    Zs = round(Zs, res_i)
    Zl = round(Zl, res_i)

    temp1 = math.pow(10, res_i)
    res = 1 / temp1

    limits = open(resource_path('Limits.csv'), 'w', newline='')
    lmt_write = csv.writer(limits, delimiter = ',')
    Xnew, Ynew, Znew = 0, 0, 0
    Xs1, Ys1, Zs1 = 0, 0, 0
    if Xs < 0:
        Xnew = abs(int(round(Xs, res_i) * temp1))
        Xs1 = abs(Xs)
        Xs = 0
        X = (Xl + Xs1 - Xs)
        Xmax = X / res
        Xmax = round(Xmax, 0)
    else:
        X = (Xl - Xs)
        Xmax = X / res
        Xmax = round(Xmax, 0)
    if Ys < 0:
        Ynew = abs(int(round(Ys, res_i) * temp1))
        Ys1 = abs(Ys)
        Ys = 0
        Y = (Yl + Ys1 - Ys)
        Ymax = Y / res
        Ymax = round(Ymax, 0)
    else:
        Y = (Yl - Ys)
        Ymax = Y / res
        Ymax = round(Ymax, 0)
    if Zs < 0:
        Znew = abs(int(round(Zs, res_i) * temp1))
        Zs1 = abs(Zs)
        Zs = 0
    lmt_write.writerow([Xs, Xl + Xs1, Ys, Yl + Ys1, Zs, Zl + Zs1, Xmax + 1, Ymax + 1])

    # np.around([0.374, 1.648], decimals=2) use this for rounding input data to 2 decimal places
    XYZC3 = open(location1, 'r')
    r3 = csv.reader(XYZC3)
    p = []
    x = []
    y = []
    z = []
    #i = 1
    if r_skip == 0:
        for line in r3:
            Xinp = float(line[en_x])
            Yinp = float(line[en_y])
            Zinp = float(line[en_z])
            Xinp = round(Xinp, res_i)
            Yinp = round(Yinp, res_i)
            Xinp = round(Xinp / res)
            Yinp = round(Yinp / res)
            Zinp = round(Zinp / res)
            x.append(Xinp)
            y.append(Yinp)
            z.append(Zinp)
            #i = i + 1
    else:
        cn_skip = 0 # count skipped rows
        for line in r3:
            if cn_skip < r_skip:
                cn_skip += 1
            else:
                Xinp = float(line[en_x])
                Yinp = float(line[en_y])
                Zinp = float(line[en_z])
                Xinp = round(Xinp, res_i)
                Yinp = round(Yinp, res_i)
                Xinp = round(Xinp / res)
                Yinp = round(Yinp / res)
                Zinp = round(Zinp / res)
                x.append(Xinp)
                y.append(Yinp)
                z.append(Zinp)
    XYZC3.close()
    
    XYZC = open(temp_loc + 'csv_modified.csv', 'w', newline='')
    csv_write = csv.writer(XYZC, delimiter = ',')

    i = 0
    while (i < len(x)):
        csv_write.writerow([x[i] + Xnew, y[i] + Ynew, z[i] + Znew])
        i = i + 1
    #print("i: ", i)
    #print("Done")
    return Xs1, Ys1, Zs1

#if __name__ == '__main__':
#    multiprocessing.freeze_support()