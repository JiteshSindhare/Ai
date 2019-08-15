%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Assignment 1 - Question 1. 2019
%
%    Killer Sudoku
%
%   Jitesh Sindhare 
%   07/08/2019
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

include "alldifferent.mzn";
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% i. Read and process data (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


int:n;
array[int,int] of int:problem;
int: len::add_to_output=card(index_set_1of2(problem));
int: height::add_to_output=card(index_set_2of2(problem));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ii. Define variables (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Rows and columns for sudoku
set of int:rows=1..n;
set of int:columns=1..n;
%length and height of cage
set of int:le=1..len;
set of int:he=1..height;

int: s=3;
set of int: sub_square=1..3;
%to show which place has which number in sudoku
array[rows,columns] of var 1..n:data::add_to_output;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iii. Add the appropriate constraints (10 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% all different in  rows
constraint forall(i in rows , j in columns)(alldifferent([data[i,j] | i in rows]));
% all different in  columns
constraint forall(i in rows , j in columns)(alldifferent([data[i,j] | j in columns]));
% all different in  box
constraint forall(a,b in sub_square)(alldifferent([data[(a-1)*s+c,(b-1)*s+d]| c,d in sub_square]));
% all different in  cage
constraint forall(i in le )
(alldifferent([ data[problem[i,k],problem[i,j]] | j,k in he where j<height-1 /\ problem[i,j]>0 /\ problem[i,k]>0 /\ j mod 2 =0 /\ k=j-1 /\ k<j]));
%function to add all the elements of cage
function var int: sum_check(array[int] of var int:x)=sum(i in index_set(x))(x[i]);
% constraining that all elements of cage should be equal to the number assigned to it
constraint forall(i in le )(
(sum_check([data[problem[i,k],problem[i,j]] | j,k in he where j<height /\ problem[i,j]>0 /\ problem[i,k]>0 /\ j mod 2 =0  /\ k=j-1 /\ k<j])=problem[i,height]));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iv. Solve solution and output in a logical way (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


output  [ show_int(1,data[i,j]) ++ " " ++ 
         if j mod s == 0 then "|" else "" endif ++
         if j == n then
             if i != n then 
                if i mod s == 0 then "\n---------------------\n" else "\n" endif 
         else "" endif else "" endif  
    | i in rows, j in columns] ++ ["\n"];