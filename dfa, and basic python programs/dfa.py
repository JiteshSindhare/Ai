import os
# function prototype was given already as part of the assignment. rest is done by me
""" File name:   dfa.py
    Author:      <Jitesh Sindhare>
    Date:        <3/03/2019>
    Description: This file defines a function which reads in
                 a DFA described in a file and builds an appropriate datastructure.

                 There is also another function which takes this DFA and a word
                 and returns if the word is accepted by the DFA.

                 It should be implemented for Exercise 3 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""

"""assigning values to variables according after checking first word of the files while traversing each line if they are transition
initial or accepting state.
Considering the test3 which has states which is more than one character so i had to take states as whole word.
where a[0], a[1] are the words numbered accordingly and v1 v2 v3 are the sattes, since their scope was very small so they are 
named small"""
def load_dfa(path_to_dfa_file):
    """ This function reads the DFA in the specified file and returns a
        data structure representing it. It is up to you to choose an appropriate
        data structure. The returned DFA will be used by your accepts_word
        function. Consider using a tuple to hold the parts of your DFA, one of which
        might be a dictionary containing the edges.

        We suggest that you return a tuple containing the names of the start
        and accepting states, and a dictionary which represents the edges in
        the DFA.

        (str) -> Object
    """
# idea of using line.split() came form here
# https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python

    # YOUR CODE HERE
    initial_state=0
    accepting_states=[]
    edges={}
    with open(path_to_dfa_file) as dfa_file:

        for line in dfa_file:
            a=line.split()      # using line.split() to read line word by word
            if(a[0]=='initial'):
                initial_state=a[-1][-1]
                if(a[1][0]=='o'):
                    initial_state=a[1]

            elif(a[0]=='accepting'):
                for i in range(len(a)):
                    if i>0:
                        if(a[i][0]=='s'):
                            accepting_states.append(a[i][5:])
                        elif(a[i][0]=='o'):
                            accepting_states.append(a[i][:])
                        elif(a[i][0]=='z'):
                            accepting_states.append(a[i][:])

            elif(a[0]=='transition'):

                if (a[1][0] == 's'):
                    v1=a[1][5:]
                    v2=a[2][5:]
                    v3=a[3]
                    if(v1 in edges.keys()):
                        vgh=[v3,v2]
                        vold = edges[v1].append(vgh)

                    else:
                        n=[v3,v2]
                        edges[v1]=n
                elif (a[1][0] == 'o'):

                    v1=a[1]
                    v2=0
                    v3=0

                    if(a[2][0]=='z'):

                        v2=a[2]
                        v3 = a[3]
                    elif(a[2][0]=='o'):

                        v2=a[2]
                        v3 = a[3]

                    if(v1 in edges.keys()):

                        vgh=[v3,v2]
                        vold = edges[v1].append(vgh)
                    else:
                        edges[v1]=[v3,v2]

                elif (a[1][0] == 'z'):

                    v1=a[1]
                    v2 = 0
                    v3 = 0

                    if (a[2][0] == 'z'):

                        v2=a[2]
                        v3 = a[3]
                    elif (a[2][0] == 'o'):

                        v2=a[2]
                        v3 = a[3]

                    if (v1 in edges.keys()):

                        vgh=[v3,v2]
                        vold = edges[v1].append(vgh)  # v3= label and v2= edge

                    else:
                        vgm=[v3,v2]
                        edges[v1] = [v3, v2]
    tup1=(initial_state,accepting_states,edges)
    return tup1


"""In the function below, there is a loop running till the length of the word that is passsed to the function,  and the argument dfa 
consist of the initial sate and accepting_states ad edges which are appropriately assigned to the variable, and in each iteration 
it is checked accordingly and then updating current_state and at last after iterating over each character of the word if the 
current satte is not in accepting state then it is returns false otherwise True"""
def accepts_word(dfa, word):
    """ This function takes in a DFA (that is produced by your load_dfa function)
        and then returns True if the DFA accepts the given word, and False
        otherwise.

        (Object, str) -> bool
    """
    # YOUR CODE HERE

    initial_state=dfa[0]
    accepting_states=dfa[1]
    edges=dfa[2]
    current_state=initial_state
    #In the loop below i is the index of the character and word[i] has the current character we are processing
    for i in range(len(word)):
        #I am checking length of edge of current state because of the limitation of the way they are stored when there are more than 2
        #edges present
        if i==0:
            if len(edges[current_state])==2:
                if word[i]==edges[current_state][0] :
                    current_state=edges[current_state][1]

                    continue
            else:
                for j in range(len(edges[current_state])):
                    if j <=1:
                        if edges[current_state][0]==word[i] :
                            current_state=edges[current_state][1]

                            break
                        else:
                            continue
                    elif j>1:
                        if word[i]==str(edges[current_state][j][0]):
                            current_state=edges[current_state][j][1]
                            break
                        else:
                            continue
        else:
            if len(edges[current_state])>2:
                for k in range( len(edges[current_state])    ):
                    if k<=1:
                        if edges[current_state][0] == word[i] :
                            current_state = edges[current_state][1]

                            break

                    elif k > 1:
                        if word[i] == edges[current_state][k][0] :
                            current_state = edges[current_state][k][1]

                            break
            elif len(edges[current_state])==2:
                if word[i]==edges[current_state][0] :
                    current_state=edges[current_state][1]

                    continue
                else:

                    continue

    if(current_state in accepting_states):
        return True
    else:
        return False



