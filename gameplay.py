
from board import check_winner, createBoard, get_player_move, make_move, printBoard, switch_turn
from agent import minimax


def game_controller():
    board = createBoard()

    play_ai = input("Play against AI? (y/n): ").lower() == 'y'
    ai_player = None
    ai_depth = 2
    if play_ai:
        human_side = input("Do you wanna be an Attacker (A) or Defender (D)? ").upper()
        ai_player = 'A' if human_side == 'D' else 'D'
        diff = input("Difficulty - 1 (Easy), 2 (Medium), 3 (Hard): ")
        ai_depth = int(diff) if diff.isdigit() * 2 - 1 else 3


    printBoard(board)
    current_player = 'A'
    while True:
        print(f"---- Turn: {current_player}")

        if play_ai and current_player == ai_player:
            print("AI is thinking...")
            _, best_move = minimax(board, ai_depth, float('-inf'), float('inf'), True, current_player, ai_player)

            if best_move:
                ro, co, rt, ct, piece = best_move
                make_move(board, ro, co, rt, ct, piece)
            else:
                print("AI is stuck")
                break
        else:

            r1, c1, r2, c2 = get_player_move()
            if not make_move(board, r1, c1, r2, c2, current_player):
                continue

        printBoard(board)
        # check for a win
        status = check_winner(board)
        if status != "Ongoing":
            print(f"GAME OVER! Result: {status}")
            break

        current_player = switch_turn(current_player)

    
def main():
    game_controller()

if __name__ == "__main__":
    main()