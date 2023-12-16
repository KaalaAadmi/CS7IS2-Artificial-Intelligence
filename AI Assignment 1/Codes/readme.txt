NOTE: In my system, python is the alias used instead of python3. So, if your system uses the alias python3, then you would need to modify the commands respectively. Same for pip.
 
Before running the codes, you need to install the following dependency:
	- pyamaze
		- To install it, use the following command:
			pip install pyamaze

To run the algorithms as per the questions:
- To run the Search Algorithms together:
	- python starter1.py
- To run the MDP algorithms together:
	- python starter2.py
- To run all the algorithms together:
	- python starter3.py

To run the algorithms individually:
- Search Algorithms:
	- Breadth First Search:
		- python breadth_first_search.py
	- Depth First Search:
		- python depth_first_search.py
	- A-Star:
		- python a_star.py
-MDP Algorithms:
	- Value Iteration:
		- python value_iteration.py
	-Policy Iteration:
		- python policy_iteration.py

To run the python script which calculates the average values of:
- Search Algorithms:
	- python calculator_search.py
- MDP Algorithms:
	- python calculator_mdp.py
- All Algorithms:
	- python calculator_all.py

NOTE: All of the scripts on running would ask for the user to input the size of the maze to be generated which will then be used by the algorithms to find a path from the start to the goal cell. The start cell is (0,0) and the goal cell is (row, column)th cell.