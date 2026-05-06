def createBoard(size=11):
    board = [['.' for i in range(size)] for i in range(size)]
    mid = size // 2
    board[mid][mid] = 'K'
    for d in [1, 2]:
        board[mid + d][mid] = 'D'
        board[mid - d][mid] = 'D'
        board[mid][mid + d] = 'D'
        board[mid][mid - d] = 'D'

    for dr in [-1, 1]:
        for dc in [-1, 1]:
            board[mid + dr][mid + dc] = 'D'

    for i in range((mid//2)+1):
            board[mid+i][0] = 'A'
            board[mid+i][size-1] = 'A'
            board[mid-i][0] = 'A'
            board[mid-i][size-1] = 'A'
            board[0][mid+i] = 'A'
            board[size-1][mid+i] = 'A'
            board[0][mid-i] = 'A'
            board[size-1][mid-i] = 'A'
            board[mid][1] = 'A'
            board[1][mid] = 'A'
            board[mid][size-2] = 'A'
            board[size-2][mid] = 'A'
    return board


def printBoard(board):
    for row in board:
        print(' '.join(row))
    print()

# def moveUp(board, player, c, r, steps):
#     board[r][c] = ''
#     board[r-steps][c] = player

# def moveDown(board, player, c, r, steps):
#     board[r][c] = ''
#     board[r+steps][c] = player

# def moveRight(board, player, c, r, steps):
#     board[r][c] = ''
#     board[r][c+steps] = player

# def moveLeft(board, player, c, r, steps):
#     board[r][c] = ''
#     board[r][c-steps] = player

def make_move(board, r1, c1, r2, c2, player):
    if not is_valid_move(board, r1, c1, r2, c2, player):
        print("Invalid move!")
        return False

    board[r1][c1] = '.'
    board[r2][c2] = player

    check_capture(board, r2, c2)
    return True

def is_valid_move(board, r1, c1, r2, c2, player):
    size = len(board)
    corners = [(0,0), (0,size-1), (size-1,0), (size-1,size-1)]
    
    if(r2 < 0 or c2 < 0 or r2 >= size or c2 >= size):
        return False
    
    if(r1 == r2 and c1 == c2):
        return False
    
    if(r1 != r2 and c1 != c2):
        return False
    
    if (r2, c2) in corners and player != 'K':
        return False
    
    if r2 == size // 2 and c2 == size // 2 and player != 'K':
        return False
    
    if board[r1][c1] != player:
        return False

    if board[r2][c2] != '.':
        return False
    
    if r1 == r2:
        step = 1 if c2 > c1 else -1
        for c in range(c1 + step, c2, step):
            if board[r1][c] != '.':
                return False

    else: 
        step = 1 if r2 > r1 else -1
        for r in range(r1 + step, r2, step):
            if board[r][c1] != '.':
                return False

    return True


def switch_turn(player):
    return 'D' if player == 'A' else 'A'

def get_player_move():
    move = input("enter your move (r1 c1 r2 c2): ")
    try:
        r1, c1, r2, c2 = map(int, move.split())
    except ValueError:
        print("Invalid input format. Please enter four integers separated by spaces.")
        return get_player_move()
    return r1, c1, r2, c2

def find_king(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 'K':
                return (r, c)
    return None


def check_capture(board, r, c):
    player = board[r][c]
    if player == '.' or player == 'K': 
        return
        
    enemy = 'A' if player == 'D' else 'D'
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    size = len(board)
    mid = size // 2
    throne = (mid, mid)
    corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]

    for dr, dc in directions:
        r1, c1 = r + dr, c + dc     
        r2, c2 = r + 2*dr, c + 2*dc 

        if 0 <= r1 < size and 0 <= c1 < size and 0 <= r2 < size and 0 <= c2 < size:
            if board[r1][c1] == enemy:
                if board[r2][c2] == player or (r2, c2) == throne or (r2, c2) in corners:
                    board[r1][c1] = '.'

def is_king_captured(board, r, c):
    if board[r][c] != 'K':
        return False

    size = len(board)
    corners = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    blocked_sides = 0

    for dr, dc in directions:
        nr, nc = r + dr, c + dc

        if not (0 <= nr < size and 0 <= nc < size):
            blocked_sides += 1
   
        elif (nr, nc) in corners:
            blocked_sides += 1

        elif board[nr][nc] == 'A':
            blocked_sides += 1

    return blocked_sides == 4

def check_winner(board):
    size = len(board)
    corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
    
    king_pos = find_king(board) 
    if king_pos is None:
        return "Attacker Wins"

    if king_pos in corners:
        return "Defender Wins"
        
    if is_king_captured(board, king_pos[0], king_pos[1]):
        return "Attacker Wins"
        
    return "Ongoing"
