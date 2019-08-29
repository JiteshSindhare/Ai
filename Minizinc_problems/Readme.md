Some problems in minizinc.
1.) Killer- is killer sudoku problem like how its stated in this site -https://www.dailykillersudoku.com/
it contains a cage and the number in the corner of cage shows what the sum of all number in cage should be.
 where n= 9 (sides length/height of sudoku)
problem= 2D array of  position of cages.
for e.g in this below diagram
and input_file.dzn file will contain following parameter.
 
n= 9
problem=[0,0,0,1,9|
	    0,2,0,3,0,4,15|
		0,6,1,5,1,6,2,5,22|
		0,7,1,7,4|
		0,8,1,8,16|
	     0,9,1,9,2,9,3,9,15|
		1,0,1,1,2,0,2,1,25|
		............|]


2.) Navy - battleship navy solitaire a sample is given in this site. 	https://lukerissacher.com/battleships
The total number of cells that ships occupy in a row or column is specified.Additionally, some cells might be known to contain water or a part of a ship. Individual ships are always surrounded
by water, even diagonally. You also know the composition of the enemy fleet, i.e., how many ships and of what size.
an example input_file.dzn will contain parameters like.
n=15( sides of board.)
col_counts=[2,1,3,3,2,0,5,4,1,1,5,5,1,0,1](cells that ship occupy in that specific column)
row_counts=[0,3,2,2,4,2,4,3,1,5,1,1,4,2,0] (cells that ship occupy in that specific row)
shipw_lengths=[5,4,4,3,3,3,2,2,2,2,1,1,1,1] (how many ships of each length are there)
starting_water=[4,4|
			14,15|](contains 2D array of coordinates where water is in initially)
starting_ships[5,2|
		    9,1|
		    7,2|
		    11,5|
		    7,7|
		    9,1](contains 2D array of coordinates where ships or piece of ship is initially)

3.) lab- scheduling labratory robots





killer sudoku image- https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjZy92tqqjkAhWBWX0KHXejBHsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FKiller_sudoku&psig=AOvVaw1jAQPX6SA5rlu43KCh06Jo&ust=1567176700851375
