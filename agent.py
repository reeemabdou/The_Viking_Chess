import copy 
from board import is_valid_move, check_winner, check_capture, switch_turn

def evaluate_board(board, player):
    score = 0
    size = len(board)
    a_count = 0
    d_count = 0
    king_pos = None

    for r in range(size):
        for c in range(size):
            if board[r][c] == 'A':
                a_count += 1
            elif board[r][c] == 'D':
                d_count += 1
            elif board[r][c] == 'K':
                d_count += 1
                king_pos = (r, c)


    if player == 'A':
        score += (a_count * 10) - (d_count  * 10)
    else:
        score += (d_count * 10) - (a_count * 10)

    if king_pos:
        kr, kc = king_pos
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        min_dist = min(abs(kr - cr) + abs(kc - cc) for cr, cc in corners)
        escape_score = (size * 2) - min_dist

        if player == 'D':
            score += escape_score * 20
        else:
            score -= escape_score * 20

    return score

def get_all_possible_moves(board, current_turn):
    moves = []
    size = len(board)
    target_pieces = ['A'] if current_turn == 'A' else ['D', 'K']

    for ro in range(size):
        for co in range(size):
            piece = board[ro][co]
            if piece in target_pieces:
                for rt in range(size):
                    if is_valid_move(board, ro, co, rt, co, piece):
                        moves.append((ro, co, rt, co, piece))

                for ct in range(size):
                    if is_valid_move(board, ro, co, ro, ct, piece):
                        moves.append((ro, co, ro, ct, piece))

    return moves

def minimax(board, depth, alpha, beta, is_maximizing, current_turn, ai_player):
    status = check_winner(board)
    if status == "Attacker Wins":
        return (10000 if ai_player == 'A' else -10000), None
    elif status == "Defender Wins":
        return (10000 if ai_player == 'D' else -10000), None
    
    if depth == 0:
        return evaluate_board(board, ai_player), None
    
    possible_moves = get_all_possible_moves(board, current_turn)

    if not possible_moves:
        return evaluate_board(board, ai_player), None

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for move in possible_moves:
            ro, co, rt, ct, piece = move
            mock_board = copy.deepcopy(board)

            mock_board[ro][co] = '.'
            mock_board[rt][ct] = piece

            check_capture(mock_board, rt, ct)

            next_turn = switch_turn(current_turn)
            eval_score, _ = minimax(mock_board, depth - 1, alpha, beta, False, next_turn, ai_player)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
                        
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in possible_moves:
            ro, co, rt, ct, piece = move
            mock_board = copy.deepcopy(board)

            mock_board[ro][co] = '.'
            mock_board[rt][ct] = piece
            check_capture(mock_board, rt, ct)

            next_turn = switch_turn(current_turn)
            eval_score, _ = minimax(mock_board, depth - 1, alpha, beta, True, next_turn, ai_player)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move