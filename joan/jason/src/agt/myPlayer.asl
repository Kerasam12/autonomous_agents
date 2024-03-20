
/*

Implementation of a Tic-Tac-Toe player that just plays random moves.

When the agent is started it must first perform a 'sayHello' action.
Once all agents have done this, the game or tournament starts.

Each turn the agent will observe the following percepts:

- symbol(x) or symbol(o) 
	This indicates which symbol this agent should use to mark the cells. It will be the same in every turn.

- a number of marks:  e.g. mark(0,0,x) , mark(0,1,o) ,  mark(2,2,x)
  this indicates which cells have been marked with a 'x' or an 'o'. 
  Of course, in the first turn no cell will be marked yet, so there will be no such percept.

- round(Z)
	Indicates in which round of the game we are. 
	Since this will be changing each round, it can be used by the agent as a trigger to start the plan to determine
	its next move.

Furthermore, the agent may also observe the following:

- next 
	This means that it is this agent's turn.
  
- winner(x) or winner(o)
	If the game is over and did not end in a draw. Indicates which player won.
	
- end 
	If the game is finished.
	
- After observing 'end' the agent must perform the action 'confirmEnd'.

To mark a cell, use the 'play' action. For example if you perform the action play(1,1). 
Then the cell with coordinates (1,1) will be marked with your symbol. 
This action will fail if that cell is already marked.

*/



/* Initial beliefs and rules */
punctuation("00", 0).
punctuation("01", 0).
punctuation("02", 0).
punctuation("10", 0).
punctuation("11", 0).
punctuation("12", 0).
punctuation("20", 0).
punctuation("21", 0).
punctuation("22", 0).

// First, define a 'cell' to be a pair of numbers, between 0 and 2. i.e. (0,0) , (0,1), (0,2) ... (2,2).

isCoordinate(0).
isCoordinate(1).
isCoordinate(2).

isCell(X,Y) :- isCoordinate(X) & isCoordinate(Y).



/* A cell is 'available' if it does not contain a mark.*/
available(X,Y) :- isCell(X,Y) & not mark(X,Y,_).

// Check that a cell is a lateral cell
isLateral(X, Y) :- available(X, Y) & ((X == 0 & Y == 1) | 
								   (X == 1 & Y == 0) |
								   (X == 1 & Y == 2) |
								   (X == 2 & Y == 1) ).

// Check that a cell is a corner cell
isCorner(X, Y) :- available(X, Y) & ((X == 0 & Y == 0) | 
								  (X == 0 & Y == 2) |
								  (X == 2 & Y == 0) |
								  (X == 2 & Y == 2) ).
// Check that a cell is the center cell

isCenter(X, Y) :- available(X,Y) & (X == 1 & Y == 1).

// A cell is occupied by oponent
occupiedByOponent(X,Y) :- not available(X, Y) & mark(X, Y, Z). 
occupiedByMyself(X,Y) :- not available(X, Y) & mark(X, Y, symbol(S)).

checkWinnerMove(X,Y) :- ((occupiedByMyself(X+1,Y+1) & occupiedByMyself(X-1,Y-1)) | 
						(occupiedByMyself(X-1,Y+1) & occupiedByMyself(X+1,Y-1)) | 
						(occupiedByMyself(X+1,Y) & occupiedByMyself(X-1,Y)) |
						(occupiedByMyself(X,Y+1) & occupiedByMyself(X,Y-1)) |
						(occupiedByMyself(X+1,Y) & occupiedByMyself(X+2,Y)) |
						(occupiedByMyself(X-1,Y) & occupiedByMyself(X-2,Y)) |
						(occupiedByMyself(X,Y+1) & occupiedByMyself(X,Y+2)) |
						(occupiedByMyself(X,Y-1) & occupiedByMyself(X,Y-2)) |
						(occupiedByMyself(X+1,Y+1) & occupiedByMyself(X+2,Y+2)) |
						(occupiedByMyself(X-1,Y-1) & occupiedByMyself(X-2,Y-2)) ).

checkLoserMove(X,Y) :- ((occupiedByOponent(X+1,Y+1) & occupiedByOponent(X-1,Y-1)) | 
						(occupiedByOponent(X-1,Y+1) & occupiedOponent(X+1,Y-1)) | 
						(occupiedByOponent(X+1,Y) & occupiedByOponent(X-1,Y)) |
						(occupiedByOponent(X,Y+1) & occupiedByOponent(X,Y-1)) |
						(occupiedByOponent(X+1,Y) & occupiedByOponent(X+2,Y)) |
						(occupiedByOponent(X-1,Y) & occupiedByOponent(X-2,Y)) |
						(occupiedByOponent(X,Y+1) & occupiedByOponent(X,Y+2)) |
						(occupiedByOponent(X,Y-1) & occupiedByOponent(X,Y-2)) |
						(occupiedByOponent(X+1,Y+1) & occupiedByOponent(X+2,Y+2)) |
						(occupiedByOponent(X-1,Y-1) & occupiedByOponent(X-2,Y-2)) ).	
						

//A values of heuristic

checkDiagonalA1(X,Y) :- available(X,Y) & (available(X+1, Y+1)& available(X-1, Y-1))|(occupiedByMyself(X+1, Y+1)& not occupiedByOponent(X-1, Y-1))|(occupiedByMyself(X-1, Y-1)& not occupiedByOponent(X+1, Y+1)).
checkDiagonalA2(X,Y) :- available(X,Y) & (available(X-1, Y+1)& available(X+1, Y-1))|(occupiedByMyself(X-1, Y+1)& not occupiedByOponent(X+1, Y-1))|(occupiedByMyself(X+1, Y-1)& not occupiedByOponent(X-1, Y+1)).

checkLateralVerA(X,Y) :- available(X,Y) & (available(X+1, Y)& available(X-1, Y))|(occupiedByMyself(X+1, Y)& not occupiedByOponent(X-1, Y))|(occupiedByMyself(X-1, Y)& not occupiedByOponent(X+1, Y)).
checkLateralHorA(X,Y) :- available(X,Y) & (available(X, Y+1)& available(X, Y+2))|(occupiedByMyself(X, Y+1)& not occupiedByOponent(X, Y+2))|(occupiedByMyself(X, Y+2)& not occupiedByOponent(X, Y+1)).

checkLateralHorInvA(X,Y) :- available(X,Y) & (available(X, Y-1)& available(X, Y-2))|(occupiedByMyself(X, Y-1)& not occupiedByOponent(X, Y-2))|(occupiedByMyself(X, Y-2)& not occupiedByOponent(X, Y-1)).

checkVerUpA(X,Y) :- available(X,Y) & (available(X-1, Y)& available(X-2, Y))|(occupiedByMyself(X-1, Y)& not occupiedByOponent(X-2, Y))|(occupiedByMyself(X-2, Y)& not occupiedByOponent(X-1, Y)).
checkVerDownA(X,Y) :- available(X,Y) & (available(X+1, Y)& available(X+2, Y))|(occupiedByMyself(X+1, Y)& not occupiedByOponent(X+2, Y))|(occupiedByMyself(X+2, Y)& not occupiedByOponent(X+1, Y)).

checkHorMidA(X,Y) :- available(X,Y) & (available(X, Y-1)& available(X, Y+1))|(occupiedByMyself(X, Y-1)& not occupiedByOponent(X, Y+1))|(occupiedByMyself(X, Y+1)& not occupiedByOponent(X, Y-1)).


//A values of heuristic
checkDiagonal1(X,Y) :- available(X,Y) & (available(X+1, Y+1)& available(X-1, Y-1))|(occupiedByMyself(X+1, Y+1)& not occupiedByOponent(X-1, Y-1))|(occupiedByMyself(X-1, Y-1)& not occupiedByOponent(X+1, Y+1)).
checkDiagonal2(X,Y) :- available(X,Y) & (available(X-1, Y+1)& available(X+1, Y-1))|(occupiedByMyself(X-1, Y+1)& not occupiedByOponent(X+1, Y-1))|(occupiedByMyself(X+1, Y-1)& not occupiedByOponent(X-1, Y+1)).

checkLateralVer(X,Y) :- available(X,Y) & (available(X+1, Y)& available(X-1, Y))|(occupiedByMyself(X+1, Y)& not occupiedByOponent(X-1, Y))|(occupiedByMyself(X-1, Y)& not occupiedByOponent(X+1, Y)).
checkLateralHor(X,Y) :- available(X,Y) & (available(X, Y+1)& available(X, Y+2))|(occupiedByMyself(X, Y+1)& not occupiedByOponent(X, Y+2))|(occupiedByMyself(X, Y+2)& not occupiedByOponent(X, Y+1)).

checkLateralHorInv(X,Y) :- available(X,Y) & (available(X, Y-1)& available(X, Y-2))|(occupiedByMyself(X, Y-1)& not occupiedByOponent(X, Y-2))|(occupiedByMyself(X, Y-2)& not occupiedByOponent(X, Y-1)).

checkVerUp(X,Y) :- available(X,Y) & (available(X-1, Y)& available(X-2, Y))|(occupiedByMyself(X-1, Y)& not occupiedByOponent(X-2, Y))|(occupiedByMyself(X-2, Y)& not occupiedByOponent(X-1, Y)).
checkVerDown(X,Y) :- available(X,Y) & (available(X+1, Y)& available(X+2, Y))|(occupiedByMyself(X+1, Y)& not occupiedByOponent(X+2, Y))|(occupiedByMyself(X+2, Y)& not occupiedByOponent(X+1, Y)).

checkHorMid(X,Y) :- available(X,Y) & (available(X, Y-1)& available(X, Y+1))|(occupiedByMyself(X, Y-1)& not occupiedByOponent(X, Y+1))|(occupiedByMyself(X, Y+1)& not occupiedByOponent(X, Y-1)).

//A values of heuristic
xPlusA1(X,Y) :- (available(X+1,Y)|(occupiedByMyself(X+1,Y))) & not occupiedByOponent(X+1, Y).  
xMinusA1(X,Y) :- (available(X-1,Y)|(occupiedByMyself(X-1,Y))) & not occupiedByOponent(X-1, Y).
yMinusA1(X,Y) :- (available(X,Y-1)|(occupiedByMyself(X,Y-1))) & not occupiedByOponent(X, Y-1).  
yPlusA1(X,Y) :- (available(X,Y+1)|(occupiedByMyself(X,Y+1))) & not occupiedByOponent(X, Y+1). 


// T values of the heuristic
middlecheckdiagonalT1(X,Y) :- available(X,Y) & (occupiedByOponent(X+1,Y+1) | occupiedByOponent(X-1,Y-1)).
middlecheckdiagonalT2(X,Y) :- available(X,Y) & (occupiedByOponent(X-1,Y+1) | occupiedByOponent(X+1,Y-1)).
middlecheckverticalT(X,Y) :- available(X,Y) & (occupiedByOponent(X+1,Y) | occupiedByOponent(X-1,Y)).
middlecheckhorizontalT(X,Y) :- available(X,Y) & (occupiedByOponent(X,Y+1) | occupiedByOponent(X,Y-1)).

left2rightT(X,Y) :- available(X,Y) & (occupiedByOponent(X, Y-1) | occupiedByOponent(X,Y-2)).
right2leftT(X,Y) :- available(X,Y) & (occupiedByOponent(X, Y+1) | occupiedByOponent(X,Y+2)).

top2downT(X,Y) :- available(X,Y) & (occupiedByOponent(X+1, Y) | occupiedByOponent(X+2,Y)).
down2upT(X,Y) :- available(X,Y) & (occupiedByOponent(X-1, Y) | occupiedByOponent(X-2,Y)).

diagonalupleftT(X,Y) :- available(X,Y) & (occupiedByOponent(X-1,Y-1) | occupiedByOponent(X-2,Y-2)).
diagonaluprightT(X,Y) :- available(X,Y) & (occupiedByOponent(X-1,Y+1) | occupiedByOponent(X-2,Y+2)).
diagonaldownleftT(X,Y) :- available(X,Y) & (occupiedByOponent(X+1,Y+1) | occupiedByOponent(X+2,Y+2)).
diagonaldownrightT(X,Y) :- available(X,Y) & (occupiedByOponent(X+1,Y-1) | occupiedByOponent(X+2,Y-2)).




started.


/* Plans */





/* When the agent is started, perform the 'sayHello' action. */
+started <- sayHello.

/* Whenever it is my turn, play a random move. Specifically:
	- find all available cells and put them in a list called AvailableCells.
	- Get the length L of that list.
	- pick a random integer N between 0 and L.
	- pick the N-th cell of the list, and store its coordinates in the variables A and B.
	- mark that cell by performing the action play(A,B).
*/
+round(Z) : next <- 
					Win = _;
					Lose = _;
					Cent = _;
					Corner = _;
					Lat = _;
					A = _;
					B = _;

					.findall(available(X,Y), checkWinnerMove(X,Y), Win);
					.findall(available(X,Y), checkLoserMove(X,Y), Lose);
					.findall(available(X,Y), isCenter(X,Y), Cent);
					.findall(available(X,Y), isCorner(X,Y), Corner);
					.findall(available(X,Y), isLateral(X,Y), Lat);


					if (.length(Win) > 0){
						L = .length(Win);
						N = math.floor(math.random(L));
						.nth(N,Win,available(A,B));
						play(A,B);
					} 
					

					if (.length(Lose) > 0){
						L = .length(Lose);
						N = math.floor(math.random(L));
						.nth(N,Lose,available(A,B));
						play(A,B);
						} 
					if (.length(Cent) > 0){
						L = .length(Cent);
						N = math.floor(math.random(L));
						.nth(N,Cent,available(A,B));
						play(A,B);

					} 
					if (.length(Corner) > 0){
						L = .length(Corner);
						N = math.floor(math.random(L));
						.nth(N,Corner,available(A,B));
						play(A,B);
					}
					if (.length(Lat) > 0){
						L = .length(Lat);
						N = math.floor(math.random(L));
						.nth(N,Lat,available(A,B));
						play(A,B);
					}.

					


						

						 
						 
/* If I am the winner, then print "I won!"  */
+winner(S) : symbol(S) <- .print("I won!").

+end <- confirmEnd.
