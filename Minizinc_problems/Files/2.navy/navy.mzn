%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Assignment 1 - Question 2. 2019
%
%    Navy Solitaire
%
%   Jitesh Sindhare
%   11/08/2019
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
include "globals.mzn";
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% i. Read and process data (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% taking 30 secs in geocode

int:n;
array[int] of int:col_counts;
array[int] of int:row_counts;
array[int] of int:ship_lengths;
array[int,int] of int:starting_water;
array[int,int] of int :starting_ships;
int:row=card(index_set(row_counts));
int:col=card(index_set(col_counts));
set of int:rows=1..row;
set of int:cols=1..col;
int:len_ships=card(index_set(ship_lengths));
int:max_size::add_to_output=max(i in 1..len_ships)(ship_lengths[i]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ii. Define variables (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

array[rows,cols] of var 0..max_size:grid::add_to_output;
int:rc=row*col;
var bool:check=false;
array[rows,cols] of var bool:track;
array[1..rc] of var 0..max_size:grid_1d=[grid[i,j]|i in rows,j in cols];
int:r_sw::add_to_output=card(index_set_1of2(starting_water));
int:c_sw::add_to_output=card(index_set_2of2(starting_water));
int:r_ss::add_to_output=card(index_set_1of2(starting_ships));
int:c_ss::add_to_output=card(index_set_2of2(starting_ships));
array[1..max_size,1..len_ships] of var 0..infinity:ship_count;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iii. Add the appropriate constraints (10 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% initially where we have water
constraint forall(i in 1..r_sw, j in 1..c_sw where j mod 2=0 /\ i mod 2=1)(grid[starting_water[i,j-1],starting_water[i,j]]=0);
% initially all the ships we have in grid
constraint forall(i in 1..r_ss, j in 1..c_ss where j mod 2=0 /\ 1 mod 2=1)(grid[starting_ships[i,j-1],starting_ships[i,j]]!=0);

% counting a row to see if the number of ships there are equal to the number of ships availabe in ship_lengths
constraint forall(i in rows)((sum(j in cols)(grid[i,j]!=0))=row_counts[i]);

% counting a column to see if the number of ships there are equal to the number of ships availabe in ship_lengths
constraint forall(j in cols)((sum(i in rows)(grid[i,j]!=0))=col_counts[j]);


% to keep track of all the indexes which are checked for being in sequence , so that they don't mess up.
predicate track_ij(var int:i,var int:j,var int:v1,var int:v2)=forall(a in i..v1,b in j..v2)(track[i,j]=true);


% To make entries in ship_count according to number of ship of ship sizes count
constraint forall(k in 1..len_ships)(ship_count[ship_lengths[k],k]=(count(ship_lengths,ship_lengths[k])+sum(i in 1..len_ships)(ship_lengths[i]>ship_lengths[k])));

% constraining that no more than given number of ship size will be there in our grid
constraint forall(k in 1..len_ships)((ship_count[ship_lengths[k],k])=(count(grid_1d,ship_lengths[k])));

% To change grids to original if the predicate which is making sure of sequence in row or in column fails
predicate reco_seq2(var int:i,var int:j,var bool:b,var int:v1,var int:v2)=if j!=v2 then reco_seq2(i,j+1,check,v1,v2) /\ grid[i,j+1]=grid[i,j]+1 endif;
predicate reco_seq(var int:i,var int:j,var bool:b,var int:v1,var int:v2)=if i!=v1 then reco_seq2(i+1,j,check,v1,v2) /\ grid[i+1,j]=grid[i,j]+1 endif;

% To make sure numbers/ships are in sequence in a row
predicate seq2(var int:i,var int:j,var bool:b,var int:v1,var int:v2)=if grid[i,j]!=1 then if j>1 /\ grid[i,j]>=j then grid[i,j-1]=grid[i,j]-1 /\  seq2(i,j-1,b,v1,v2)else b=false /\ reco_seq2(i,j,b,v1,v2)  endif else b=true /\ track_ij(i,j,v1,v2)endif;

% To make sure numbers/ships are in sequence in a column
predicate seq(var int:i,var int:j,var bool:b,var int:v1,var int:v2)=if grid[i,j]!=1 then if i>1 /\ grid[i,j]>=i then seq(i-1,j,b,v1,v2) /\ grid[i-1,j]=grid[i,j]-1 else b=false /\ reco_seq(i,j,b,v1,v2)
 endif else b=true /\ track_ij(i,j,v1,v2) endif;

% To make sure no two neighbouring indexes are of same value apart form being 0 i.e. water
constraint forall(i in rows,j in cols where i>1 /\ j>1 /\ i<row /\ j<col /\ grid[i,j]!=0)(grid[i,j]!=grid[i-1,j] /\ grid[i,j]!=grid[i+1,j] /\ 
grid[i,j]!=grid[i,j-1] /\ grid[i,j]!=grid[i,j+1] /\
grid[i,j]!=grid[i-1,j-1] /\ grid[i,j]!=grid[i+1,j+1] /\ 
grid[i,j]!=grid[i+1,j-1] /\ grid[i,j]!=grid[i-1,j+1]);

% making calls to predicates which constrains for being numbers in sequence
constraint forall(i in rows,j in cols where not track[i,j])((if grid[i,j]>1 then if not seq(i,j,check,i,j) then seq2(i,j,check,i,j) else seq(i,j,check,i,j) endif endif));

% Constrains that all four corners(diagonals) of a number is a zero
constraint forall(i in rows,j in cols where  j>1/\i>1/\i<row /\j<col /\ grid[i,j]>0)(grid[i-1,j-1]=0 /\ grid[i+1,j+1]=0 /\ grid[i+1,j-1]=0 /\ grid[i-1,j+1]=0 );
% Constrains that for any positive number always there will be a smaller number before it in same row or in same column
constraint forall(i in rows,j in cols where j>1/\i>1 /\ grid[i,j]>0)( grid[i-1,j]=grid[i,j]-1 \/ grid[i,j-1]=grid[i,j]-1);

% constraints that any number in the grid will only be equal or smaller than the row and column it is in
constraint forall(i in rows,j in cols)(grid[i,j]<=i /\ grid[i,j]<=j);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iv. Solve the problem and output in a logical way (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%???
output  [  show_int(1,grid[i,j])  ++ " " ++ 
         if j == n then
             if i != n then 
                if i mod col == 0 then "\n\n" else "\n" endif 
         else "" endif else "" endif  
    | i in 1..row, j in 1..col] ++ ["\n"];
    