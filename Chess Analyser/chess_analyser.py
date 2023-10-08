import chess.engine
import chess.pgn
import io

print(
    "NOTES FOR USE: Black advantage is positive, white is negative, and the PGN you paste in should be all on one line. Best way to use it is with a chess app that allows you to replay games but not analyze. To figure out who is threatening mate, the first time it says mate in, check who played that move, and their opponent is threatening mate. E.G. If the 22nd move was mate in, white is threatening mate."
)
print("")
want_board = input("Enter 1 if you want the chessboard to show after every move ")

# Path to the Komodo engine binary
komodo_path = "Macengine/komodo-14.1-64-bmi2-osx"

# Define the thresholds for move ratings
INACCURACY_THRESHOLD = 100
MISTAKE_THRESHOLD = 200
BLUNDER_THRESHOLD = 400


def get_move_rating(eval_before, eval_after, is_black_turn, actual_move, move1):
    # Handle "Mate in" situations
    if isinstance(eval_before, str) and eval_before.startswith("Mate in"):
        return ""  # Ignore 'Mate in' situations

    # Handle "Mate in" situations for eval_after
    if isinstance(eval_after, str) and eval_after.startswith("Mate in"):
        return ""  # Ignore 'Mate in' situations for eval_after

    # Convert eval_before and eval_after to integers
    eval_before = int(eval_before)
    eval_after = int(eval_after)

    eval_change = eval_before - eval_after

    if is_black_turn:
        if actual_move == move1:
            return "Best Move"
        if eval_change >= 400:
            return "Blunder"
        if eval_change >= 200:
            return "Mistake"
        if eval_change >= 100:
            return "Inaccuracy"
    else:
        if actual_move == move1:
            return "Best Move"
        if eval_change <= -400:
            return "Blunder"
        if eval_change <= -200:
            return "Mistake"
        if eval_change <= -100:
            return "Inaccuracy"

    return "Good Move"


def main():
    board = chess.Board()

    # Prompt the user to input the PGN content
    pgn_content = input("Paste the PGN content here:\n")

    # Parse the user-provided PGN content
    try:
        pgn_game = chess.pgn.read_game(io.StringIO(pgn_content))
    except ValueError as e:
        print(f"Error parsing PGN: {e}")
        return

    # Create a UCI chess engine process
    with chess.engine.SimpleEngine.popen_uci(komodo_path) as engine:
        is_black_turn = False
        move_number = 1  # Initialize move number
        total_moves = len(list(pgn_game.mainline_moves()))  # Get total number of moves
        prev_eval = 0  # Initialize previous evaluation
        white_inaccuracy = 0
        white_mistake = 0
        white_blunder = 0
        white_good_move = 0
        white_best_move = 0
        black_inaccuracy = 0
        black_mistake = 0
        black_blunder = 0
        black_good_move = 0
        black_best_move = 0
        best_move = None
        move1 = "Any could"

        for move in pgn_game.mainline_moves():
            board.push(move)

            # Get engine evaluation before the move
            eval_before = prev_eval
            eval_after = 0

            # The input string
            input_string = str(best_move)

            # Find the position of "move=" in the string
            start_index = input_string.find("move=")

            # Extract the move value, assuming it is in the format move=value,
            if start_index != -1:
                end_index = input_string.find(",", start_index)
                if end_index != -1:
                    if move_number > 2:
                        move1 = input_string[
                            start_index + len("move=") : end_index
                        ].strip()

            # Check if it's Black's turn
            best_move = engine.play(board, chess.engine.Limit(time=0.1))
            if is_black_turn:
                evaluation = engine.analyse(board, chess.engine.Limit(time=0.1))

                # Handle mate evaluation
                if evaluation.get("score"):
                    if evaluation["score"].relative.is_mate():
                        mate_in = evaluation["score"].relative.mate()
                        score = f"Mate in {mate_in}"  # Display positive for Black
                    else:
                        score = -evaluation["score"].relative.score()
                else:
                    score = 0
            else:
                evaluation = engine.analyse(board, chess.engine.Limit(time=0.1))
                # Handle mate evaluation
                if evaluation.get("score"):
                    if evaluation["score"].relative.is_mate():
                        mate_in = evaluation["score"].relative.mate()
                        score = f"Mate in {-mate_in}"  # Display negative for White
                    else:
                        score = evaluation["score"].relative.score()
                else:
                    score = 0

            actual_move = move.uci()
            print(
                f"Move {move_number}/{total_moves}: {move.uci()} - Evaluation: {score}",
                end=" ",
            )

            # Check if the evaluation contains "Mate in" and handle it separately
            if "Mate in" in str(score):
                move_rating = ""
            else:
                move_rating = get_move_rating(eval_before, score, is_black_turn, actual_move, move1)

                # Count inaccuracies, mistakes, and blunders
                if is_black_turn:
                    if move_rating == "Inaccuracy":
                        black_inaccuracy += 1
                    elif move_rating == "Mistake":
                        black_mistake += 1
                    elif move_rating == "Blunder":
                        black_blunder += 1
                    elif move_rating == "Good Move":
                        black_good_move += 1
                    elif move_rating == "Best Move":
                        black_best_move += 1
                else:
                    if move_rating == "Inaccuracy":
                        white_inaccuracy += 1
                    elif move_rating == "Mistake":
                        white_mistake += 1
                    elif move_rating == "Blunder":
                        white_blunder += 1
                    elif move_rating == "Good Move":
                        white_good_move += 1
                    elif move_rating == "Best Move":
                        white_best_move += 1

            if (
                isinstance(eval_before, str)
                and eval_before.startswith("Mate in")
                or isinstance(eval_after, str)
                and eval_after.startswith("Mate in")
                or "Mate in" in str(score)
            ):
                print("")
            else:
                print(f"- Move Rating: {move_rating}")

            print(f"{move1} was the best move")

            if want_board == "1":
                print(board)
                print("")
                print("")

            # Toggle the turn indicator
            is_black_turn = not is_black_turn
            move_number += 1  # Increment move number
            prev_eval = score

            # Check if it's the second last move
            if move_number == total_moves:
                white_accuracy = round(
                    100
                    * (
                        1
                        - (white_blunder + white_inaccuracy + white_mistake)
                        / (
                            white_blunder
                            + white_inaccuracy
                            + white_mistake
                            + white_good_move
                            + white_best_move
                        )
                    ),
                    1,
                )
                black_accuracy = round(
                    100
                    * (
                        1
                        - (black_blunder + black_inaccuracy + black_mistake)
                        / (
                            black_blunder
                            + black_inaccuracy
                            + black_mistake
                            + black_good_move
                            + black_best_move
                        )
                    ),
                    1,
                )
                print("White moves")
                print(f"{white_best_move} best moves")
                print(f"{white_good_move} good moves")
                print(f"{white_inaccuracy} inaccuracies")
                print(f"{white_mistake} mistakes")
                print(f"{white_blunder} blunders")
                print(f"{white_accuracy}% accuracy")
                print("")
                print("Black moves")
                print(f"{black_best_move} best moves")
                print(f"{black_good_move} good moves")
                print(f"{black_inaccuracy} inaccuracies")
                print(f"{black_mistake} mistakes")
                print(f"{black_blunder} blunders")
                print(f"{black_accuracy}% accuracy")
                break  # Stop the evaluation on the second last move

            if board.is_checkmate():
                print("Checkmate!")


if __name__ == "__main__":
    main()
