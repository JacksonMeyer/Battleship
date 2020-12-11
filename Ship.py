from random import randint

# class for a ship object and needed functions
class Ship:
  # constructer for ship object
  def __init__(self, size, direction, location):
    self.size = size
    
    if direction == 'hor' or direction == 'vert':
      self.direction = direction
    else:
      raise ValueError("Must use hor or vert")
    
    if direction == 'hor':
      if location['row'] in range(total_rows):
        self.coordinates = []
        for val in range(size):
          if location['col'] + val in range(total_cols):
            self.coordinates.append({'row': location['row'], 'col': location['col'] + val})
       
    
    if direction == 'vert':
      if location['col'] in range(total_cols):
        self.coordinates = []
        for val in range(size):
          if location['row'] + val in range(total_rows):
            self.coordinates.append({'row': location['row'] + val, 'col': location['col']})
          
    if self.full():
      print_board(board)
      print(" ".join(str(row_col) for row_col in self.coordinates))
    else:
      self.setBoard()
   
   #function to check if the board is full
  def full(self):
    for row_col in self.coordinates:
      if board[row_col['row']][row_col['col']] == 1:
        return True
    return False
  
  
  # function to set the board
  def setBoard(self):
    for row_col in self.coordinates:
      board[row_col['row']][row_col['col']] = 1
  
  # function for checking if a locatin contains coords
  def contain(self, location):
    for row_col in self.coordinates:
      if row_col == location:
        return True
    return False

  # function for if a ship has been sunk
  def sunk(self):
    for row_col in self.coordinates:
      if board_view[row_col['row']][row_col['col']] == 'O':
        return False
    return True

  
# settings for the game

num_ships = 4
total_rows = 9 
total_cols = 9 
upper_size = 5
lower_size = 2

# users selects difficulty
while True:
    try:
      diff = int(input("Select difficulty. 1:Easy, 2:Medium, 3:Hard "))
      if diff == 1:
          print("Easy mode. 60 turns")
          max_shots = 60
          break
      elif diff == 2:
          print("Medium mode. 40 turns")
          max_shots = 40
          break
      elif diff == 3:
          print("Hard mode. 20 turns")
          max_shots = 20
          break
      else:
        print("Not a difficulty")     
    except ValueError:
      print("Enter numerical value that corrersponds to difficulty")


# objects for the game
ships = []
board = [[0] * total_cols for x in range(total_rows)]
board_view = [["O"] * total_cols for x in range(total_rows)]

# functions for our game

#prints the board
def print_board(board_array):
  print("\n  " + " ".join(str(x) for x in range(1, total_cols + 1)))
  for r in range(total_rows):
    print(str(r + 1) + " " + " ".join(str(c) for c in board_array[r]))
  print()

# function for checking when randomly placing our ships
def check(size, direction):
  locations = []

  if direction == 'hor':
    if size <= total_cols:
      for r in range(total_rows):
        for c in range(total_cols - size + 1):
          if 1 not in board[r][c:c+size]:
            locations.append({'row': r, 'col': c})
  if direction == 'vert':
    if size <= total_rows:
      for c in range(total_cols):
        for r in range(total_rows - size + 1):
          if 1 not in [board[i][c] for i in range(r, r+size)]:
            locations.append({'row': r, 'col': c})

  if not locations:
    return 'None'
  else:
    return locations

# function that randomly places the ships on the board
def rand_gen():
  size = randint(lower_size, upper_size)
  direction = 'hor' if randint(0, 1) == 0 else 'vert'

  locations = check(size, direction)
  if locations == 'None':
    return 'None'
  else:
    return {'location': locations[randint(0, len(locations) - 1)], 'size': size,\
     'direction': direction}

# function to get a row and value
def get_row():
  while True:
    try:
      guess = int(input("Row Guess: "))
      if guess in range(1, total_rows + 1):
        return guess - 1
      else:
        print("Not a number on the board")
    except ValueError:
      print("Enter numerical value")

# function to get a col and value
def get_col():
  while True:
    try:
      guess = int(input("Column Guess: "))
      if guess in range(1, total_cols + 1):
        return guess - 1
      else:
        print("Not a number on the board")
    except ValueError:
      print("Enter numerical value")


# randomly put ships on board

counter = 0
while counter < num_ships:
  rand_ship = rand_gen()
  if rand_ship == 'None':
    continue
  else:
    ships.append(Ship(rand_ship['size'], rand_ship['direction'], rand_ship['location']))
    counter += 1

print_board(board_view)
 
#loop that plays the game
for turn in range(max_shots):
  print("Turn:", turn + 1)
  print(max_shots - turn , "turns left")
  print("Ships still floating:", len(ships))
  print()
  
  guesses = {}
  while True:
    guesses['row'] = get_row()
    guesses['col'] = get_col()
    if board_view[guesses['row']][guesses['col']] == 'X' or \
     board_view[guesses['row']][guesses['col']] == '*':
      print("You guessed that one already.")
    else:
      break


  ship_hit = False
  for ship in ships:
    if ship.contain(guesses):
      print("Your guess was a hit")
      ship_hit = True
      board_view[guesses['row']][guesses['col']] = 'X'
      if ship.sunk():
        print("Ship has been sunk")
        ships.remove(ship)
      break
  if not ship_hit:
    board_view[guesses['row']][guesses['col']] = '*'
    print("Your guess missed")

  print_board(board_view)
  
  if not ships:
    break

# determine the result
print("Game over")
if ships:
  print(len(ships), "ships got away. You lose")
else:
  print("Ships are all sunk. You won")