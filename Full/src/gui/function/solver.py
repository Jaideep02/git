#solve(bo), is a backtracking algorithm that solves the Sudoku puzzle. 
#It takes a single argument, bo, which is the current state of the puzzle.
#The function uses a nested loop to iterate through all the empty cells in the puzzle,
#and for each empty cell it tries all the numbers from 1 to 9. 
#If a number is valid for the current cell, the function places that number in the cell
#and recursively calls itself to check the next empty cell. 
#If no number is valid for the current cell, the function backtracks and tries a different number.
#If the function successfully solves the puzzle, it returns True, otherwise it returns False.
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

#valid(bo, num, pos), takes three arguments: bo is the current state of the puzzle,
#num is the number to be placed in the current cell, and pos is the position of the current cell
#in the form of a tuple (row, col). The function checks whether the number num is valid for the current
#cell by checking the current row, column, and 3x3 subgrid that the cell belongs to, and returns True if 
#the number is valid and False otherwise.
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

#find_empty(bo), takes a single argument, bo, which is the current state of the puzzle.
#The function uses a nested loop to iterate through all the cells in the puzzle and returns the 
#position of the first empty cell it finds, in the form of a tuple (row, col), or None if there are no more
#empty cells. This function is used by the backtracking algorithm to determine which cell to fill in next.
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None