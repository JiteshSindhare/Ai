% Assignment 1 - Question 3. 2019
%
%    Lab Robot Problem
%
%   Jitesh Sindhare
%   12/08/2019

int: n;                   % Number of jobs
int: m;                  % Activities per job
int: b;                   % Number of banks
int: cap;               % Number of activities that can be processed in parallel

set of int: jobs::add_to_output = 1..n;    
set of int: banks = 1..b;
set of int: locations = 1..n; 
set of int: activities = 1..m;
set of int: activity_pairs = 1..m-1;

array [jobs, activities] of int: durations;
array [jobs, activities] of int: minlags;
array[jobs, activities] of int:maxlags;
%array[jobs, activity_pairs] of int:maxlags;
array [jobs, activities] of 0..1: robot_required;
%robot_required = 1 if bank robot is required or 0 if main robot is required.

array [jobs] of int: x_pos = [((job-1) div b)+1 | job in jobs];
array [jobs] of int: bank = [((job-1) mod b)+1 | job in jobs];
array [jobs, jobs] of int: travel_time = array2d(jobs, jobs, [ceil(sqrt(pow(abs(x_pos[l_1]-x_pos[l_2]),2) + pow(abs(bank[l_1]-bank[l_2]),2)))   | l_1 in locations, l_2 in locations ]);
 
 
 include "cumulative.mzn";
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% i. Infer a maximum time horizon (2.5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% because there will be no next activity after the last activity so no need to add maxlag for last activity.
int: horizon::add_to_output= max(i in jobs)(sum(k in activities)(if k!=m then durations[i,k]+maxlags[i,k] else durations[i,k] endif));


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ii. Define decision variables for the starting time of each activity (2.5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % Hint call decision variables start and output to console, i.e.,  start ::add_to_output;
%???
array [jobs, activities] of var 0..horizon:start::add_to_output;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iii. Define a no_overlap predicate that takes into account travel time (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     
                                              
 predicate sequence_travel_time(array[int] of var int: start,
                     array[int] of int: dur,
                     array[int] of int: location,
                     array[int,int] of int: travel_time) = forall(k,l in jobs,i,j in index_set(start)
 where i!=j /\ k=j mod n+1 /\ l=i mod n+1 /\ k!=l)(start[i]+dur[i]+travel_time[location[l],location[k]]<=start[j] \/ start[j]+dur[j]+travel_time[location[k],location[l]]<=start[i]);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iv. Add the following constraints (20 marks)
%     - minimum timelags
%     - maximum timelags
%     - Power capacity constraint
%     - No-overlap for the main-robot
%     - No-overlap for each bank-robot
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%???
%  HOW TO SET IT BETWEEN CONSECUTIVE OPERATIONS
%  for minlag

constraint forall(i in jobs,j in activities,l in jobs,k in activities where i!=l \/ j!=k  )( start[i,j]>=start[l,k]+minlags[l,k] );
%constraint forall(i in jobs,j in activities,l in jobs,k in activities where (i!=l \/ j!=k)  )( if  start[i,j]>start[l,k] then start[i,j]-start[l,k]= minlags[l,k] endif);
% for max lag  THINK ABOUT THIS - ((i>=l) \/ (i<l))
constraint forall(i in jobs,j in activities,l in jobs,k in activities where i!=l \/ j!=k  )( start[l,k]+maxlags[l,k]>=start[i,j] );
%constraint forall(i in jobs,j in activities,l in jobs,k in activities where (i!=l \/ j!=k) /\ j<m /\ k<m )(if i=1 then start[i,j+1]<=start[l,k]+maxlags[l,k] else start[i,j]<=start[l,k]+maxlags[l,k] endif);

% power capcity constraint  j!=m /\ ((i>=l) \/ (i<l)) replaced by i!=l \/ j!=m
%constraint sum(i in jobs,j in activities,l in jobs,m in activities where j!=m /\ ((i>=l) \/ (i<l)) )(start[i,j]=start[l,m])=cap;
% constraint cumulative([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],[ robot_required[i,j] |i in jobs,j in activities],cap);
constraint cumulative([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],main_robo,cap);
constraint cumulative([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],bank_robo,cap);

% constraint cumulative([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],[main_robo[i,j] |i in jobs , j in activities],cap);
% constraint cumulative([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],[bank_robo[i,j] |i in jobs , j in activities ],cap);

% below one is for when i separated robot_required based on its value of 0 and 1 so below one is value of array 1 when robo_req[]!=1
% array[jobs,activities] of int:main_robo=[if if robot_required[i,j]=0 then 1 else 0 endif | i in jobs,j in activities];
% array[jobs,activities] of int:bank_robo=[if if robot_required[i,j]=1 then 1 else 0 endif | i in jobs,j in activities];


array[1..m*n] of int:main_robo=[ if robot_required[i,j]=0 then 1 else 0 endif | i in jobs,j in activities];
array[1..m*n] of int:bank_robo=[ if robot_required[i,j]=1 then 1 else 0 endif | i in jobs,j in activities];

%constraint forall(i in jobs, j in activities)(if robot_required[i,j]=0 then main_robo[i,j]=1 else main_robo[i,j]=0 endif);
%constraint forall(i in jobs, j in activities)(if robot_required[i,j]=1 then bank_robo[i,j]=1 else bank_robo[i,j]=0  endif);
%constraint cumulative([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],[ if robot_required[i,j]=1 then 0 else 1 endif |i in jobs,j in activities],cap);



%no-overlap for the main-robot
% constraint forall(i in jobs,j in activities,l in jobs,m in activities where robot_required[i,j]=0 /\ robot_required[l,m]=0 /\ (i!=l \/ j!=m) )(( start[i,j]>=start[l,m]+minlags[l,m] /\ start[i,j]<=start[l,m]+maxlags[l,m] ) \/ (start[l,m]>=start[i,j]+minlags[i,j] /\ start[l,m]<=start[i,j]+maxlags[i,j] ));
constraint forall(i in jobs,j in activities where robot_required[i,j]=0)(sequence_travel_time([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],x_pos,travel_time));



% no-overlap for bank robot
% constraint forall(i in jobs,j in activities,l in jobs,m in activities where robot_required[i,j]=1 /\ robot_required[l,m]=1 /\ (i!=l \/ j!=m) )( ( start[i,j]>=start[l,m]+minlags[l,m] /\ start[i,j]<=start[l,m]+maxlags[l,m] ) \/ (start[l,m]>=start[i,j]+minlags[i,j] /\ start[l,m]<=start[i,j]+maxlags[i,j] ));

constraint forall(i in jobs,j in activities where robot_required[i,j]=1)(sequence_travel_time([start[i,j]|i in jobs,j in activities],[durations[i,j]|i in jobs,j in activities],x_pos,travel_time));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% v. Add search annotations to represent (10 marks)
%    - list heuristic
%    - least slack, i.e., pick the variables with the minimum latest start time - earliest start time
%    - earliest first, i.e., pick the variable with the minimum earliest start time
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ann: list_heuristic = int_search([start[i,j]| i in jobs, j in activities ],input_order,indomain_min,complete);
ann: least_slack = int_search([start[i,j]| i in jobs, j in activities ],first_fail,indomain_min,complete);

ann: earliest_first = int_search([start[i,j]| i in jobs, j in activities ],smallest,indomain_min,complete);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% vi. Add the objective function (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

var 0..horizon: makespan ::add_to_output = max(i in jobs, j in activities)(start[i,j]+durations[i,j]);
solve::list_heuristic  minimize makespan;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% vii. Complete the following (5 marks)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% The optimal solution to tiny.dzn is ???
% After 20 seconds solve time on realistic.dzn the different search annotations find the following solution
% list_heuristic = ???
% least_slack = ???
% earliest_first = ???


