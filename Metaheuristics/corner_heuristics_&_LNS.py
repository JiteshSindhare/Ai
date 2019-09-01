#!/usr/bin/env python
# coding: utf-8

# # Assignment 2: 2-Pack

# In[1]:


from framework import *
from math import  sqrt
from random import sample,shuffle,randint,random

# ## Problem Description
# 
# The problem considers a set of $n$ rectangular boxes that are to be packed into a set of $m$ containers. Each box and each container has an $x$-length and a $y$-length. Furthermore each box as an associated weight $w$ that represents how important it is that the box is packed into a container. A box can either be packed vertically or horizontally into the container. The aim of the problem is to pack as many boxes into containers as possible such that the sum of the weights of packed boxes is maximised. Note that boxes cannot overlap and must stay within the boundaries of the containers. A solution to a problem with four containers and 100 boxes is visualised below.
# 
# 
# ![title](images/lab2.png)
# 
# 

# ## Data
# 
# A number of data files have been generated. Data files are in the following format
# 
# $n$
# 
# $x^{container}_1$ $y^{container}_1$ 
# 
# $x^{container}_2$ $y^{container}_2$ 
# 
# ...
# 
# $x^{container}_n$ $y^{container}_n$
# 
# $m$
# 
# $x^{box}_1$ $y^{box}_1$ $w^{box}_1$ 
# 
# $x^{box}_2$ $y^{box}_2$ $w^{box}_2$
# 
# ...
# 
# $x^{box}_m$ $y^{box}_m$ $w^{box}_m$
# 

# ## Part 1: Corner Heuristic (50 marks)
# 
# ## Corner Heuristic
# 
# An efficient heuristic for the 2d packing problem can be developed that is based on a couple of insights: (1) we may as well pack in corners and (2) corners are easy to track. To do so, for all empty containers we only consider the bottom-left corner as the initial corner. When we insert a box into that container we check whether the box can be placed (both horizontally and vertically) into that corner. A box can fit into a specific corner in a container in a specific direction if firstly the box fits inside the container, and secondly it does not overlap any other boxes that are already placed in the container. Once a box is inserted into a corner we can create two new corners - one at the top-left corner of the box, and one at the bottom-right corner of the box. In the image below, we see how the corners progress as boxes are inserted into a container. 
# 
# 
# ![title](images/corners.png)
# 
# If a box cannot fit into any of the corners from any of the containers then in the final solution it remains
# unpacked. Note that the order that both the boxes and containers are considered by the heuristic will most likely
# produce different solutions, as well as the order corners are considered by a box and whether the box first
# attempts to be inserted horizontally or vertically.
# 
# Part 1 of the assignment will consider implementing this heuristic. Template code is given but only to generate an
# initial solution. Please rewrite the functions (including function parameters!) as required.
# 
# 

# **1a) Complete a function to check whether a box can be inserted into a specific corner of a container in a
# specific direction (i.e., either horizontally or vertically) (10 marks)** - Note a position is infeasible if
# any part of the box is outside the container or if the box overlaps with any other box that are already positioned
# in the container

# In[2]:

def distance(x1,y1,x2,y2):
    return sqrt(((x2-x1)**2)+((y2-y1)**2))

def candidate_box_line_points(box,corner,is_horizontal):
    """
    :param box: box is the rectangular package we are getting.
    :return: all four sides/lines of a rectangular box.
    """
    point1=(corner.x,corner.y)
    point2=(corner.x,(corner.y+(box.y_length if is_horizontal else box.x_length)))
    point3=((corner.x+(box.x_length if is_horizontal else box.y_length) ),corner.y)
    point4=(corner.x + (box.x_length if is_horizontal else box.y_length), corner.y +(box.y_length if is_horizontal else box.x_length))
    return [(point1,point2),(point2,point4),(point3,point4),(point1,point3)]
def line_points(box):
    """
    :param box: box is the rectangular package we are getting.
    :return: all four sides/lines of a rectangular box.
    """
    point1=(box.x_min,box.y_min) # bottom left
    point2=(box.x_min,(box.y_min+box.y_delta)) # left top
    point3=((box.x_min+box.x_delta),box.y_min) # bottom right
    point4=(box.x_min + box.x_delta, box.y_min + box.y_delta) # top right
    return [(point1,point2),(point2,point4),(point3,point4),(point1,point3)]

def line_equation(point1,point2):
    """
    :param point1: 1st point , i.e. x1,y1
    :param point2: 2nd point , i.e. x2,y2
    :return: since we only have two type of lines horizontal or vertical, so line equation won't be complex.
    Horizontal line if y1==y2 so m=0. so, y=y-intercept . i.e. y=(y1)
    vertical line if x1==x2 so m=undefined. so x=x-intercept. i.e. x=(x1)
    """
    if (point2[1]-point1[1])==0:
        y=point2[1]
        return ("y{}".format(y),(point1,point2))

    if (point2[0]-point1[0])==0:
        x=point2[0]

        return ("x{}".format(x),(point1,point2))

def is_intersecting(str1,str2,container,box):
    """
    :param str1: value returned from lin_equation(equation of 1st line) of form 'x1'.((x1,y1),(x2,y2))
    :param str2: value returned from line_equation(equation of 2nd line) of form 'x1'.((x3,y3),(x4,y4))
    :return: false if they are parallel, that is line1: y=k line2: y=c,
            True and point of intersection if they have an intersection point.
    """

    if str1[0][0]==str2[0][0]:
        return False
    else:
        x=int(str1[0][1:])
        y = int(str2[0][1:])
        point1=str1[1][1]
        point2=str2[1][1]
#        if box.id>6:
        #print("str1=", str1, 'str2=', str2,'point1=',point1,"point2=",point2,"intersection points",x," ",y)

        if x==str1[1][1][0] or x==str1[1][0][0]:
            y1=str1[1][0][1]
            y2=str1[1][1][1]
            y3=str2[1][0][1]
            y4=str2[1][1][1]
            if( (y2 > y1 and y < y2 and y > y1) or (y2 < y1 and y > y2 and y < y1) ) and ( ( y3>y4 and y<y3 and y>y4)
            or ( y4>y3  and y<y4 and y>y3 )):
            #if y<point1[1] str1[1][0][1] and y:
                #print("X== STR1 str1=", str1, 'str2=', str2, 'point1=', point1, "point2=", point2, "intstn pt", x, " ", y)
                return True
            else:
                return False
        if x==str2[1][1][0] or x==str2[1][0][0] :
            y1 = str2[1][0][1]
            y2 = str2[1][1][1]
            y3=str2[1][0][1]
            y4=str2[1][1][1]
            #if (y2 > y1 and y < y2 and y > y1) or (y2 < y1 and y > y2 and y < y1):
            if ((y2 > y1 and y < y2 and y > y1) or (y2 < y1 and y > y2 and y < y1)) and (
                    (y3 > y4 and y < y3 and y > y4) or (y4 > y3 and y < y4 and y > y3)):
                #print("X==str2 str1=", str1, 'str2=', str2, 'point1=', point1, "point2=", point2, "intstn pt", x, " ",y)
                return True
            else:
                return False

        if y==str1[1][1][1] or y==str1[1][0][1] :
            x1 = str1[1][0][0]
            x2 = str1[1][1][0]
            x3 = str2[1][0][0]
            x4 = str2[1][1][0]
            #if (x2 > x1 and x < x2 and x > x1) or (x2 < x1 and x > x2 and x < x1):
            if ( (x2 > x1 and x < x2 and x > x1) or (x2 < x1 and x > x2 and x < x1) ) and (
                    (x3>x4 and x>x4 and x<x3 ) or (x4>x3 and x>x3 and x<x4 ) ):
                #print("Y==STR1 str1=", str1, 'str2=', str2, 'point1=', point1, "point2=", point2, "intstn pt", x, " ",y)
                return True
            else:
                return False

        if y==str2[1][1][1] or y==str2[1][0][1] :
            x1 = str2[1][0][0]
            x2 = str2[1][1][0]
            x3 = str2[1][0][0]
            x4 = str2[1][1][0]
#            if (x2 > x1 and x < x2 and x > x1) or (x2 < x1 and x > x2 and x < x1):
            if ((x2 > x1 and x < x2 and x > x1) or (x2 < x1 and x > x2 and x < x1)) and (
                    (x3 > x4 and x > x4 and x < x3) or (x4 > x3 and x > x3 and x < x4)):
                #print("Y==STR2 str1=", str1, 'str2=', str2, 'point1=', point1, "point2=", point2, "intstn pt", x, " ",y)
                return True
            else:
                return False
def check_placement_feasibility(container, candidate_box, is_horizontal, corner):
    if len(container.corners)==1 and corner.x==0 and corner.y==0 :
    #    print("++++++++++Corner", corner.string())
    #    container.corners=[]
        return True
        #candidate_box.pack(container.id,0,0,is_horizontal)
    elif corner.x>container.x_length or corner.y>container.y_length:
        return False
    else:

        if (corner.x>(container.x_length )):
            return False

        if  (corner.y>(container.y_length )):
            return False
        if ((corner.x + (
                candidate_box.x_length if is_horizontal else candidate_box.y_length)) > container.x_length):
            return False

        if ((corner.y + (
                candidate_box.y_length if is_horizontal else candidate_box.x_length)) > container.y_length):
            return False
        # not taking each corner from container.corners list because already those corners were getting passed in the 4th augment
        # of this function by function pack.

        if (corner.y + (candidate_box.y_length if is_horizontal else candidate_box.x_length)) <= (
                container.y_length ) and \
                (corner.x + (candidate_box.x_length if is_horizontal else candidate_box.y_length)) <= (
                container.x_length ):

            #candidate_box_line=candidate_box_line_points(candidate_box,corner,is_horizontal)
            #print('lines of ccandidate box',candidate_box_line)
            j = 0
            for box in container.boxes:
                packed_box_lines=line_points(box)
                #print('lines of packed box', packed_box_lines)
                if ((corner.x + (
                        candidate_box.x_length if is_horizontal else candidate_box.y_length)) > container.x_length):
                    return False

                if ((corner.y + (
                        candidate_box.y_length if is_horizontal else candidate_box.x_length)) > container.y_length):
                    return False

                if ((corner.x >= box.x_min) and corner.x < (box.x_min+box.x_delta)) and ((corner.y +
                ( candidate_box.y_length if is_horizontal else candidate_box.x_length)) > box.y_min) \
                        and corner.y<box.y_min :
                    return False

                if ((corner.y >= box.y_min) and corner.y < (box.y_min+box.y_delta)) and corner.x<box.x_min and( (corner.x + (
                candidate_box.x_length if is_horizontal else candidate_box.y_length)) > box.x_min):
                    return False

                if ((corner.x + (
                        candidate_box.x_length if is_horizontal else candidate_box.y_length)) > container.x_length):
                    return False

                if ((corner.y + (
                        candidate_box.y_length if is_horizontal else candidate_box.x_length)) > container.y_length):
                    return False

                if ((corner.x >= box.x_min) and corner.x < (box.x_min+box.x_delta)) and (corner.y>=box.y_min ) and \
                        corner.y<(box.y_min+box.y_delta) :
                    return False

                if (corner.y >= box.y_min) and (corner.y < (box.y_min+box.y_delta)) and (corner.x >=box.x_min) and \
                        (corner.x<(box.x_min+box.x_delta)):
                    return False

                if corner.x >= box.x_min and corner.x < (box.x_min + box.x_delta) and corner.y == box.y_min:
                    return False


                if box.y_min > corner.y:

                    if corner.x>=box.x_min and corner.x<=(box.x_min+box.x_delta) and corner.y==box.y_min:
                        return False

                    if corner.y>=box.y_min and corner.y<=(box.y_min+box.y_delta) and corner.x==box.x_min:
                        return False


                    if (corner.x>=box.x_min) and corner.x<(box.x_min+box.x_delta) and ((corner.y + (candidate_box.y_length if is_horizontal else candidate_box.x_length))>box.y_min):
                        return False

                    if (corner.y>=box.y_min) and corner.y<(box.y_min+box.y_delta) and (corner.x + (candidate_box.x_length if is_horizontal else candidate_box.y_length))>box.x_min:
                        return False

                    if corner.x >= box.x_min and corner.x < (
                            box.x_min + box.x_delta) and corner.y == box.y_min:
                        return False

                    if corner.y >= box.y_min and corner.y < (
                            box.y_min + box.y_delta) and corner.x == box.x_min:
                        return False


                    if not (box.x_min + (box.x_length if box.is_horizontal else box.y_length) < corner.x) and (
                            corner.x > box.x_min):
                        if (box.x_min + (box.x_length if box.is_horizontal else box.y_length)) > corner.y:
                            dist = distance(corner.x, corner.y, corner.x, box.y_min)

                            if is_horizontal:
                                check = candidate_box.y_length
                            else:
                                check = candidate_box.x_length

                            if dist >= check:
                                pass
                            else:
                                return False


                if box.x_min > corner.x:

                    # if is_horizontal:
                    #     check = candidate_box.x_length
                    # else:
                    #     check = candidate_box.y_length
                    if box.y_min == corner.y:
                        dist = distance(corner.x, corner.y, box.x_min, corner.y)
                        if dist >= (candidate_box.x_length if is_horizontal else candidate_box.y_length):
                            pass
                        else:
                            return False

                    if ((corner.x+(candidate_box.x_length if is_horizontal else candidate_box.y_length)))>container.x_length:
                        return False

                    if ((corner.y+(candidate_box.y_length if is_horizontal else candidate_box.x_length)))>container.y_length:
                        return False

                    if corner.x>=box.x_min and corner.x<(box.x_min+box.x_delta) and corner.y==box.y_min:
                        return False


                    if box.y_min > corner.y:


                        dist = distance(corner.x, corner.y, corner.x, box.y_min)

                        if is_horizontal:
                            check = corner.y+candidate_box.y_length
                        else:
                            check = corner.y+candidate_box.x_length
                        if dist >= check:
                            pass
                        else:
                            return False
                    if box.y_min < corner.y:
                        if (corner.x + (candidate_box.x_length if is_horizontal else candidate_box.y_length)) <= box.x_min \
                                or (box.y_min + (box.y_length if box.is_horizontal else box.x_length)) <= corner.y:
                            pass
                        else:
                            return False

                if box.y_min == corner.y and box.x_min <= corner.x:
                    if (box.x_min + (box.x_length if box.is_horizontal else box.y_length)) <= corner.x:
                        pass
                    else:
                        return False

                if box.x_min == corner.x and box.y_min >= corner.y:
                    dist = distance(corner.x, corner.y, corner.x, box.y_min)
                    if dist > (candidate_box.y_length if is_horizontal else candidate_box.x_length):
                        pass
                    else:
                        return False

                if box.y_min < corner.y and box.x_min < corner.x:

                    dist = distance(corner.x, corner.y, box.x_min, corner.y)
                    dist2 = distance(corner.x, corner.y, corner.x, box.y_min)
                    if ((corner.x >= (
                            box.x_min + box.x_delta)) and \
                        (dist >= (candidate_box.x_length if is_horizontal else candidate_box.y_length))) or \
                            ((corner.y >= ( box.y_min + box.y_delta)) and \
                             (dist2 >= (box.y_length if box.is_horizontal else box.x_length)) ):
                        pass
                    else:
                        return False
            return True

# **1b) Write a function to update the corners of a container when a box is placed into a corner in a specific direction (10 marks)** - Note that the corner into which the box is being placed can be removed from the container and new corners are added at the top-left and bottom-right of the inserted box

# In[4]:


def update_corners(container, box, is_horizontal, corner):
    if container.corners[0].x == 0 and container.corners[0].y == 0:
        container.corners.remove(corner)
    else:
        while True:
            if corner in container.corners:
                container.corners.remove(corner)
            else:
                break


    xR = corner.x + box.x_delta
    yR = corner.y
    xL = corner.x
    yL = corner.y + box.y_delta

    container.corners.append(Corner(xL, yL))
    container.corners.append(Corner(xR, yR))
    return 0


# **1c) Implement the corner heuristic (10 marks)** - Note that the heuristic should be able to generate different
# solutions depending on the input parameters, including  the order that the containers are considered, the order
# the boxes are considered, the direction preference of each box (i.e., does the heuristic try to first insert a
# box horizontally or vertically), and the corner preference of each box (i.e., what order does each box consider
# the corners of the containers).

# In[5]:


def corner_heuristic(containers, boxes,  direction_preferences, corner_preferences):
    # TODO: implement the corner heuristic as described above. Please break up functions into smaller function
    #  as required.
    # This place holder function simply adds the first box to the fix corner
    
    no_of_boxes={}
    for i in range(len(containers)):
        no_of_boxes[i]=len(containers[i].boxes)


    for index, box in enumerate(boxes):
        for container in containers:
            if box not in container.boxes:
                if pack(container, box,corner_preferences,direction_preferences):  # break
                    continue
                else:
                    continue


    return SolutionState(containers, boxes, corner_preferences, direction_preferences)



# In[6]:


def pack(container, box,direction_preferences,corners_preferences):
    # TODO: Update or delete this function as required
    number_of_corners=len(container.corners)
    for i in range(len(direction_preferences)):
        corner_got=container.corners[corners_preferences[i] % number_of_corners]

        if check_placement_feasibility(container,box,direction_preferences[i],corner_got):
            container.boxes.append(box)
            box.pack(container.id, corner_got.x, corner_got.y, direction_preferences[i])
            update_corners(container, box, direction_preferences[i], corner_got)
            return True

    for corner in container.corners:
        if check_placement_feasibility(container, box, True, corner):
            container.boxes.append(box)
            box.pack(container.id, corner.x, corner.y, True)
            update_corners(container,box,True,corner)
            return True
        elif check_placement_feasibility(container, box, False, corner):
            container.boxes.append(box)
            box.pack(container.id, corner.x, corner.y, False)
            # make_corners(container,box,True)
            update_corners(container, box, False, corner)
            return True
    return False

# **1d) Demonstrate an execution of the corner heuristic on instance file_1_20.txt (10 marks)**.
# Here we will be checking that the corners are in the correct places and that the solution is feasible.

# In[9]:
data = Data("Data/file_1_20.txt")

# shuffle(data.containers)
# shuffle(data.boxes)
#[True for box in data.boxes]
pref=[True for box in data.boxes]
for i in range(len(data.boxes)):
    if i%2==0:
        pref[i]=True
    else:
        pref[i]=False
solution = corner_heuristic(data.containers,
                            data.boxes,
                            [randint(1,100) for box in data.boxes],
                            pref)
solution.plot()
print("Solution objective is {}".format(solution.objective()))


# ### Incompleteness of the corner-heuristic
# 
# In general when building a meta-heuristic it is desirable to ensure that the heuristic being used to generate solutions is *complete*, i.e., for a given parameter setting the heuristic will generate the optimal solution. In the case where your meta-heuristic uses multiple heuristics, it is sufficient to ensure that only one of the heuristics is complete. The corner-heuristic is known to be incomplete. This means that for some problems, there does not exist a parameter setting to the heuristic that will generate an optimal solution.
# 
# **1e) Provide a minimal counter example that demonstrates that the corner heuristic is incomplete, i.e., an instance of a 2-D packing problem where no matter what parameters the heuristic is given it will never find the optimal solution. Briefly explain your answer (10 marks).**

# WRITTEN RESPONSE HERE

# ## Part 2: Large Neighbourhood Search (50 marks)
# 
# Large Neighbourhood Search (LNS) is a single-solution based metaheuristic that aims to find high quality solutions
# to optimisation problems through iteratively destroying and repairing an incumbant solution. In the second part of
# this assignment we will build a LNS to the 2D packing problem that utilises the corner heuristic. Before the
# destroy and repair iterations of the Large Neighbourhood Search can begin, we must find an initial feasible
# solution to the problem. Below is a function that creates an initial feasible solution where no boxes are backed

# In[18]:


def initial_feasible_solution(data):
	"""Takes the data and returns a feasible solution where no boxes are packed into any containers."""

	return SolutionState(containers=data.containers,
										   boxes=data.boxes,
										   corner_preferences=[0 for box in data.boxes],
										   direction_preferences=[True for index in range(len(data.boxes))])


# ### Destroy
# 
# Here we partially *destroy* a solution to our problem by completely unpacking a number of containers. In this way,
# the boxes in the packed containers remain *fixed* whereas the unpacked containers are *relaxed*. Clearly, the
# number of containers that we unpack (the *degree of destruction*) will impact how the search progresses.
# 
# **2a) Complete the following function to partially destroy a given solution by completely unpacking a number of
# containers (10 marks)**

# In[11]:


def destroy(incumbant_solution, degree_of_destruction=0.5):
    """Unpacks a certain number of containers"""
    containers=incumbant_solution.containers
    boxes=incumbant_solution.boxes
    corner_preferences=incumbant_solution.corner_preferences
    direction_preferences=incumbant_solution.direction_preferences
    # Taking random containers to destroy , like we have to destroy 2 out of 4 so which 2 out of those 4 is generated
    # randomly using random.sample
    containers_to_destroy=sample([x.id for x in containers],int(1/degree_of_destruction))

    for container in containers:
        if container.id in containers_to_destroy:
            container.unpack()
    solution=SolutionState(containers,boxes,corner_preferences,direction_preferences)
    return solution


# ### Repair
# 
# We repair a solution by using the corner-heuristic to try to reinsert the unpacked boxes. Recall that there are a number of parameters, i.e. box order, container order, corner preferences and direction preferences, that will impact how the corner heuristic will construct a solution. For example, the following parameter choices all seem reasonable
# 
# * Shuffle the boxes randomly, while keeping the remaining parameters the same as the incumbant solution
# * Order the boxes by weight in a non-increasing order, while keeping the remaining parameters the same as the
# incumbant solution
# * Order the boxes by weight / area in a non-increasing order, while keeping the remaining parameters the same as
# the incumbant solution
# * Shuffle the container order randomly, wile keeping the remaining parameters the same as the incumbant solution
# * Permute the direction preferences of some boxes, while keeping the remaining parameters the same as the incumbant
# solution
# * Modify the corner preferences of some boxes, while keeping the remaining parameters the same as the incumbant
# solution
# 
# 
# We do not want to constrain the heuristic to always use the same parameters choices and therefore wish for the
# solution to select parameters from a repair solution probabilistically.
# 
# **2b) Complete the following function to reconstruct a solution. Ensure that it is possible to exploit different
# parameters choices (at least 5) when using the corner heuristic. Briefly (in 5 lines or less) explain your approach
# (20 marks)**

# WRITTEN RESPONSE HERE

# In[13]:


def repair(solution,para_choice):
    """Repair the solution using the corner-heuristic with different parameter settings. There are a range of
    possible parameter settings"""

    choice=randint(1,6)
#    print('------------Parameter choice',choice)

    if choice==1:
        # 1.) shuffling the boxes randomly
        shuffle(solution.boxes)
        heuristic='shuffling boxes randomly'
        unchanged([solution.containers,solution.corner_preferences,solution.direction_preferences])
 #       print('sending for corner heuristics with', heuristic)
    elif choice==2:
        #2.) ordering boxes in decreasing order of their weight.
        box_order=[x for x in solution.boxes]
        quick_sort(0,len(solution.boxes)-1,box_order,False)
        solution.boxes = box_order
        solution.boxes.reverse()
        for box in solution.boxes:
            print('!',box.weight,end=' ')
        print('\n')
        heuristic=' ordering boxes in decreasing order of their weight '
        unchanged([solution.containers, solution.corner_preferences, solution.direction_preferences])
  #      print('sending for corner heuristics with', heuristic)
    elif choice==3:
        # 3.)Order the boxes by weight/area
        box_order = [x for x in solution.boxes]
        quick_sort(0, len(solution.boxes) - 1, box_order, True)
        solution.boxes = box_order
        solution.boxes.reverse()
        for box in solution.boxes:
            print('!', box.weight / (box.x_length * box.y_length), end=' ')
        print('\n')
        heuristic='ordering boxes in decreasing order by weight/area'
        unchanged([solution.containers, solution.corner_preferences, solution.direction_preferences])
   #     print('sending for corner heuristics with', heuristic)
    #box_order=solution.boxes
    elif choice==4:
        #4.) shuffly the container order randomly
        shuffle(solution.containers)
        heuristic=' shuffling container randomly'
        unchanged([solution.boxes, solution.corner_preferences, solution.direction_preferences])
    #    print('sending for corner heuristics with', heuristic)
    elif choice==5:
        #5.) permute the direction preferences of some boxes
        list_index_of_directions=[ index for index in range(len(solution.direction_preferences))]
        number_of_permutes=sample(list_index_of_directions,randint(0,len(solution.direction_preferences)))
        for i in range(len(solution.direction_preferences)):
            if i in number_of_permutes:
                value=solution.direction_preferences[i]
                solution.direction_preferences[i]= not value
        heuristic='permute/alter direction preferences of some random boxes'
        unchanged([solution.boxes,solution.containers, solution.corner_preferences])
     #   print('sending for corner heuristics with', heuristic)
    elif choice==6:
        #6.) Modify the corner preferences of some boxes.
        list_index_of_directions = [index for index in range(len(solution.direction_preferences))]
        number_of_permutes = sample(list_index_of_directions, randint(0, len(solution.direction_preferences)))
        for i in range(len(solution.corner_preferences)):
            if i in number_of_permutes:
                #value=solution.direction_preferences[i]
                solution.corner_preferences[i]= randint(0,100)
        heuristic=' modify corner preferences of some boxes'
        unchanged([solution.boxes, solution.containers, solution.corner_preferences])
      #  print('sending for corner heuristics with', heuristic)

    return corner_heuristic(solution.containers,
                            solution.boxes,
                            solution.corner_preferences,
                            solution.direction_preferences)


# In[14]:

def quick_sort(left,right,lis,area_val):

    if right-left<=0:
        return None
    else:
        if not area_val:
            pivot = lis[right].weight
        else:
            area=(lis[right].x_length)*(lis[right].y_length)
            pivot=lis[right].weight/area
        partition=partition_func(left,right,pivot,lis,right,area_val)
        quick_sort(left,partition-1,lis,area_val)
        quick_sort(partition+1,right,lis,area_val)

    return lis


def check_sublis(left_pointer, right_pointer, lis,area):
    i=left_pointer
    if not area:
        while i<right_pointer:
            if lis[left_pointer].weight==lis[right_pointer].weight:
                pass
            else:
                return False
            i+=1
    else:
        while i<right_pointer:

            if (lis[left_pointer].weight/(lis[left_pointer].x_length*lis[left_pointer].y_length))==\
                    (lis[right_pointer].weight/(lis[right_pointer].x_length*lis[right_pointer].y_length)):
                pass
            else:
                return False
            i+=1
    return True


def partition_func(left,right,pivot,lis,pi_index,area):
    left_pointer=left
    right_pointer=right-1

    while True:
        if not area:
            while lis[left_pointer].weight< pivot:
                left_pointer+=1

            while lis[right_pointer].weight >pivot and right_pointer>0 :
                right_pointer-=1

            if lis[left_pointer].weight==lis[right_pointer].weight:
                if check_sublis(left_pointer,right_pointer,lis,area):
                    break
                else:
                    pi_index_minus1=pi_index-1
                    temp_left=lis[pi_index_minus1]

                    lis[pi_index_minus1]=lis[left_pointer]
                    lis[left_pointer]=temp_left
                    left_pointer+=1

                    pi_index_plus1=pi_index+1
                    if pi_index_plus1>(len(lis)-1):
                        pi_index_plus1=pi_index_minus1-1
                    temp_right = lis[pi_index_plus1]

                    lis[pi_index_plus1]=lis[right_pointer]
                    lis[right_pointer]=temp_right
                    right_pointer-=1
        else:
            while (lis[left_pointer].weight/(lis[left_pointer].x_length*lis[left_pointer].y_length)) < pivot:
                left_pointer += 1

            while (lis[right_pointer].weight/(lis[right_pointer].x_length*lis[right_pointer].y_length)) > pivot and\
                    right_pointer > 0:
                right_pointer -= 1

            if (lis[left_pointer].weight/(lis[left_pointer].x_length*lis[left_pointer].y_length)) < pivot ==\
                    (lis[right_pointer].weight/(lis[right_pointer].x_length*lis[right_pointer].y_length)):
                if check_sublis(left_pointer, right_pointer, lis,area):
                    break
                else:
                    pi_index_minus1 = pi_index - 1
                    temp_left = lis[pi_index_minus1]

                    lis[pi_index_minus1] = lis[left_pointer]
                    lis[left_pointer] = temp_left
                    left_pointer += 1

                    pi_index_plus1 = pi_index + 1
                    if pi_index_plus1 > (len(lis) - 1):
                        pi_index_plus1 = pi_index_minus1 - 1
                    temp_right = lis[pi_index_plus1]

                    lis[pi_index_plus1] = lis[right_pointer]
                    lis[right_pointer] = temp_right
                    right_pointer -= 1
        if left_pointer>=right_pointer:
            break
        else:
            temp=lis[left_pointer]
            lis[left_pointer]=lis[right_pointer]
            lis[right_pointer]=temp

    temp=lis[left_pointer]
    lis[left_pointer]=lis[right]
    lis[right]=temp

    return left_pointer

def unchanged(list_of_objects):
	return list_of_objects


# ## Iterate
# 
# LNS works by iteratively destroying and repairing an incumbant solution. Applications of LNS often differ in how
# they update the incumbant solution. For example, the simplest version of LNS simply accepts any new solution that
# has an objective function that is at least as good as the current incumbant. This can be thought of as a
# hill-climbing method. More advanced methods, such as Simulated-Annealing, allow the possibly for the incumbant
# solution to be replaced by a solution with a worse objective.
# 
# **2c) Implement a LNS that iteratively repairs and detroys a solution using your detroy and repair operators and
# accepts a new solution if the objective is at least as good as the incumbant solution (10 marks)**

# Explanation: Here I simply used a hill-climbing acceptance criteria. My logic for doing so is that the
# neighbourhoods I am considering are quite large (i.e., the degree-of-destuction is 50% and I have a lot of
# variability in my repair operator), so I am not overly concerned about getting stuck in a local minimum.

# In[16]:


def LNSSolver(data, number_iterations):

    incumbant_solution = initial_feasible_solution(data)
    repaired_sol=incumbant_solution
    #repaired_sol=repair(incumbant_solution)
    #print('WITH iteration limit',number_iterations)
    #"""
    for i in range(number_iterations):
        des = destroy(repaired_sol)
        repaired_sol = repair(des,para_choice=[])
        if repaired_sol.objective()>incumbant_solution.objective():
            incumbant_solution=repaired_sol

    con=incumbant_solution.containers
    boxes=incumbant_solution.boxes
    print('got repaired sol')
    return SolutionState(con,boxes,[0 for box in data.boxes],[True for box in data.boxes])
    #return incumbant_solution


# **2d) Evaluate your LNS solver on instance file_4_100.txt. (10 marks)** 
# 
# Hint: You should be aiming for a solution with an objective above 800

# In[19]:

k=0
data = Data("Data/file_4_100.txt")
objec=0
while True:
    k += 1
    lns = LNSSolver(data, k)
    ob=lns.objective()
    if k==20:
        break
    if ob>objec:
        objec=ob
    elif ob>800:
        break
    else:
        continue
lns.plot()
print(objec)

# data = Data("Data/file_4_100.txt")
# lns = LNSSolver(data, 1)
# lns.plot()
# print(lns.objective())




# # **Additional Resources**
# 
# 1. There is a python library 'alns' that helps build a variant of LNS known as Adaptive Large Neighbourhood Search.
# In the examples of this library it demonstrates how to solve the
# [travelling salesman problem (TSP)](https://github.com/N-Wouda/ALNS/blob/master/examples/travelling_salesman_problem.ipynb) and the [cutting stock problem (CSP)](https://github.com/N-Wouda/ALNS/blob/master/examples/cutting_stock_problem.ipynb).
# This is vary similar to what we are trying to achieve in this assigment
# 2. Some useful references:
#   * Shaw P. (1998) Using Constraint Programming and Local Search Methods to Solve Vehicle Routing Problems. In: Maher M., Puget JF. (eds) Principles and Practice of Constraint Programming — CP98. CP 1998. Lecture Notes in Computer Science, vol 1520. Springer, Berlin, Heidelberg
#   * Pisinger, D., and Ropke, S. (2010). Large Neighborhood Search. In M. Gendreau (Ed.), Handbook of Metaheuristics (2 ed., pp. 399-420). Springer.
#   * Santini, A., Ropke, S. & Hvattum, L.M. (2018). A comparison of acceptance criteria for the adaptive large neighbourhood search metaheuristic. Journal of Heuristics 24 (5): 783-815.
