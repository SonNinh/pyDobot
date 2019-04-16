import cv2
from time import sleep, time
import numpy as np
from random import randint
from math import atan, pi, fabs, sqrt, tan


rect_width = 33
delta_dir = 10*pi/180

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged


def get_intersection(line1, line2):
    a1, b1, c1 = get_fomular_of_line(line1)
    a2, b2, c2 = get_fomular_of_line(line2)

    if a1 == 0:
        y = fabs(c1/b1)
        x = fabs((y*b2 + c2)/a2)
    elif a2 == 0:
        y = fabs(c2/b2)
        x = fabs((y*b1 + c1)/a1)
    else:
        y = fabs((c1-c2)/(b1-b2))
        x = fabs((b1*y+c1)/a1)
    return x, y


def get_center_rect(rect, ls_of_cen_dir_len):
    cross = []
    for line_v in rect[0]:
        for line_h in rect[1]:
            inter = get_intersection(ls_of_cen_dir_len[line_v], ls_of_cen_dir_len[line_h])
            cross.append(inter)
    
    x = (cross[0][0] + cross[1][0] + cross[2][0] + cross[3][0])/4
    y = (cross[0][1] + cross[1][1] + cross[2][1] + cross[3][1])/4
    
    return (int(x), int(y)), cross


def is_between_2lines(centers, lines):
    for c in centers:
        if (c[0]*lines[0][0]+c[1]*lines[0][1]+lines[0][2]) * (c[0]*lines[1][0] + c[1]*lines[1][1] + lines[1][2]) >= 0:
            return False

    return True


def get_fomular_of_line(line):
    if line[1] == 0:
        a=0.0
        b=1.0
    else:
        a = 1.0
        b = a * tan(line[1]+pi/2)
    c = -(a*line[0][0] + b*line[0][1])
    return a, b, c


def is_rect(v, h, ls_of_cen_and_dir):
    line_v = (get_fomular_of_line(ls_of_cen_and_dir[v[0]]),
              get_fomular_of_line(ls_of_cen_and_dir[v[1]]))
    center_h = (ls_of_cen_and_dir[h[0]][0], ls_of_cen_and_dir[h[1]][0])

    line_h = (get_fomular_of_line(ls_of_cen_and_dir[h[0]]),
              get_fomular_of_line(ls_of_cen_and_dir[h[1]]))
    center_v = (ls_of_cen_and_dir[v[0]][0], ls_of_cen_and_dir[v[1]][0])

    if not is_between_2lines(center_h, line_v):
        return False
    elif not is_between_2lines(center_v, line_h):
        return False
    else:
        return True


def get_distance_p2l(point, line):
    a, b, c = get_fomular_of_line(line)

    return fabs(a*point[0] + b*point[1] + c) / sqrt(a**2 + b**2)


def get_distance_l2l(line1, line2):
    return (get_distance_p2l(line1[0], line2[:2]) + get_distance_p2l(line2[0], line1[:2]))/2


def abc(lines, rect, ls_of_cen_dir_len):
    ls_of_couple_v = []
    for idx, i in enumerate(rect[0][:-1]):
        for j in rect[0][idx+1:]:
            dist_l2l = get_distance_l2l(ls_of_cen_dir_len[i], ls_of_cen_dir_len[j])
            if dist_l2l >= rect_width*0.85 and dist_l2l <= rect_width*1.15:
                ls_of_couple_v.append((i, j))
               
    ls_of_couple_h = []
    for idx, i in enumerate(rect[1][:-1]):
        for j in rect[1][idx+1:]:
            dist_l2l = get_distance_l2l(ls_of_cen_dir_len[i], ls_of_cen_dir_len[j])
            if dist_l2l >= rect_width*0.85 and dist_l2l <= rect_width*1.15:
                ls_of_couple_h.append((i, j))

    return (ls_of_couple_v, ls_of_couple_h)


def get_distance_p2p(p1, p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def find_in_neighbour(line, ls_of_cen_and_dir):
    center = line[0]
    direction = line[1]
    res = [[],[]]

    for i, each in enumerate(ls_of_cen_and_dir):
        distance = get_distance_p2p(center, each[0])
        if distance < rect_width*1.3 and distance >= rect_width*0.3:
            if fabs(direction-each[1]) < delta_dir:
                res[0].append(i)
            elif fabs(fabs(direction-each[1])-pi/2) < delta_dir:
                res[1].append(i)
        elif distance < rect_width*0.3:
            if fabs(direction-each[1]) < delta_dir:
                res[0].append(i)

    return res


def get_center_direction_len(ls_of_lines):
    res = list()

    for line in ls_of_lines:
        x1, y1, x2, y2 = line[0]
        p1 = (x1, y1)
        p2 = (x2, y2)
        line_center = [(x1+x2)//2, (y1+y2)//2]
        lenght = get_distance_p2p(p1, p2)

        if x1 == x2:
            line_direction = pi/2
        elif y1 == y2:
            line_direction = 0
        else:
            line_direction = atan((y1-y2)/(x1-x2))

        res.append([line_center, line_direction, lenght])

    return res

def retangle_detect(ls_of_lines):
    ls_of_rect = list()

    ls_of_cen_dir_len = get_center_direction_len(ls_of_lines)

    for line in ls_of_cen_dir_len:
        if line[2] > rect_width*0.2:
            ls_of_rect.append(find_in_neighbour(line, ls_of_cen_dir_len))
        # else:
        #     ls_of_rect.append[[], []]
    
    return ls_of_rect, ls_of_cen_dir_len


def main():

    while(True):
        crop_img = cv2.imread("photos/test1.png")
        # print(crop_img.dtype)
        # blur = cv2.GaussianBlur(crop_img, (15, 15), 0) # loc nhieu
        start_time = time()
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = auto_canny(gray)
        # cv2.imshow("canny", edged)
        # edged = cv2.Canny(gray, 20, 250)

        lines = cv2.HoughLinesP(edged, 1, np.pi/180, 18, 1, 7, 4)
        
        color = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
        print("num of lines:", len(lines))
        if lines is not None:
            output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.imshow("lines", output)
            ls_of_rect, ls_of_cen_dir_len = retangle_detect(lines)
            print("num of rects:", len(ls_of_rect))

            res = []
            ls_of_center_rect = []
            ls_of_cross = []
            
            for rect in ls_of_rect:
                ls_of_couple = abc(lines, rect, ls_of_cen_dir_len)
                # print(len(ls_of_couple[0]), len(ls_of_couple[1]))
                for v in ls_of_couple[0]:
                    for h in ls_of_couple[1]:
                        # output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
                        # print(v, h)
                        '''for l in v:
                            print(ls_of_cen_dir_len[l])
                            x1, y1, x2, y2 = lines[l][0]
                            cv2.line(output, (x1, y1), (x2, y2), color[0], 2)
                        for l in h:
                            print(ls_of_cen_dir_len[l])
                            x1, y1, x2, y2 = lines[l][0]
                            cv2.line(output, (x1, y1), (x2, y2), color[1], 2)'''
                        if is_rect(v, h, ls_of_cen_dir_len):
                            res.append([v, h])
                            vh = [v, h]
                            center, cross = get_center_rect(vh, ls_of_cen_dir_len)
                            added = False
                            for i in ls_of_center_rect:
                                if get_distance_p2p(center, i[0]) < rect_width*0.5:
                                    i.append(center)
                                    added = True
                                    break
                            if not added:
                                ls_of_center_rect.append([center])
                            # cv2.circle(output, center, 2, color[2], thickness=1)
                            # for cr in cross:
                            #     cv2.circle(output, (int(cr[0]),int(cr[1])), 2, color[2], thickness=1)
                                
                            # cv2.imshow("ouput", output)
                            # cv2.imshow('origin', crop_img)
                            # cv2.waitKey()
                            # break
            print("num of res:", len(res))
            final = []
            output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
            for c in ls_of_center_rect:
                x_sum = 0
                y_sum = 0
                for each in c:
                    x_sum += each[0]
                    y_sum += each[1]
                final.append((int(x_sum/len(c)), int(y_sum/len(c))))
            # for f in final:
            #     cv2.circle(crop_img, f, 2, color[2], thickness=1)
            print("num of final:", len(final))
            print("eslaped time:", time() - start_time)
            # output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
            # x1, y1, x2, y2 = lines[37][0]
            # cv2.line(output, (x1, y1), (x2, y2), color[1], 2)
            # x1, y1, x2, y2 = lines[41][0]
            # cv2.line(output, (x1, y1), (x2, y2), color[1], 2)
            # x1, y1, x2, y2 = lines[2][0]
            # cv2.line(output, (x1, y1), (x2, y2), color[1], 2)
            # x1, y1, x2, y2 = lines[20][0]
            # cv2.line(output, (x1, y1), (x2, y2), color[1], 2)
            # vh = [[37, 41],[2, 20]]
            # center, cross = get_center_rect(vh, ls_of_cen_dir_len)
            # output = np.zeros((250, 150, 3), dtype=crop_img.dtype)
            # print('asd')
            # print(ls_of_rect[15][0])
            # print(ls_of_rect[15][1])
            # for re in ls_of_rect[15][0]:
            #     x1, y1, x2, y2 = lines[re][0]
            #     cv2.line(output, (x1, y1), (x2, y2), color[0], 2)
            # for re in ls_of_rect[15][1]:
            #     x1, y1, x2, y2 = lines[re][0]
            #     cv2.line(output, (x1, y1), (x2, y2), color[1], 2)

            # for rect in ls_of_rect:
            #     output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
            #     for l in rect[0]:
            #         x1, y1, x2, y2 = lines[l][0]
            #         cv2.line(output, (x1, y1), (x2, y2), color[0], 2)
            #     for l in rect[1]:
            #         x1, y1, x2, y2 = lines[l][0]
            #         cv2.line(output, (x1, y1), (x2, y2), color[1], 2)
                
            #     cv2.imshow("ouput", output)
            #     cv2.imshow('origin', crop_img)
            #     cv2.waitKey()
            # ls_of_center_rect = []
            # ls_of_cross = []
            # for rect in res:
            #     center, cross = get_center_rect(rect, ls_of_cen_dir_len)
            #     ls_of_center_rect.append(center)
            #     ls_of_cross.append(cross)

            # print("num of res:", len(res))
            # for r in range(len(res)):
            #     output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
            #     for v in res[r][0]:
            #         x1, y1, x2, y2 = lines[v][0]
            #         cv2.line(output, (x1, y1), (x2, y2), color[0], 2)
            #     for h in res[r][1]:
            #         x1, y1, x2, y2 = lines[h][0]
            #         cv2.line(output, (x1, y1), (x2, y2), color[1], 2)
            #     cv2.circle(output, ls_of_center_rect[r], 2, color[2], thickness=1)
            #     for cr in ls_of_cross[r]:
            #         cv2.circle(output, (int(cr[0]),int(cr[1])), 2, color[2], thickness=1)
            cv2.imshow("ouput", output)
            cv2.imshow('origin', crop_img)
            cv2.waitKey()

        break
        

if __name__ == '__main__':
    main()
