import re
from typing import Tuple, Optional

from mesacheckers.ascii_renderer import ASCIIRenderer
from mesacheckers.game_controller import GameController
from mesacheckers.game_state import GameState


def parse_position(position_str: str) -> Optional[Tuple[int, int]]:
    """Parse a position string in the format 'row,col'."""
    match = re.match(r'^(\d+),(\d+)$', position_str.strip())
    if not match:
        return None
    
    row = int(match.group(1))
    col = int(match.group(2))
    
    return row, col


def main():
    print("-------------------------")
    print("----- Mesa Checkers -----")
    print("-------------------------")
    
    game_state = GameState()
    controller = GameController(game_state)
    renderer = ASCIIRenderer(game_state)

    while True:
        # -------------
        # Render game state
        # -------------

        print("\n" + renderer.render_full_game())
        
        # -------------
        # Win condition
        # -------------
        if game_state.check_win_condition(game_state.current_player):
            print(f"Player {game_state.current_player.color.name} has won!")
            break

        # -------------
        # Player's turn
        print(f"Player {game_state.current_player.color.name}'s turn")
        
        if game_state.turn_complete:
            # Optionally can inform user that we're ending the turn
            # input("Press Enter to end your turn...")
            controller.end_turn()
            continue
        
        if game_state.active_pile_position is None:
            # player needs to place a rock
            active_player_places_rock(controller)
            continue

        valid_moves = controller.get_valid_moves()

        if not valid_moves:
            print("No valid moves available.")
            game_state.turn_complete = True
            continue

        print("Valid moves:")
        for i, (row, col, max_count) in enumerate(valid_moves):
            print(f"{i + 1}: ({row}, {col}) - up to {max_count} rocks")

        action = input("Enter move number, or 'e' to end turn: ")

        if action.lower() == 'e':
            game_state.turn_complete = True
            continue

        try:
            move_index = int(action) - 1
            if not (0 <= move_index < len(valid_moves)):
                print("Invalid move number. Please try again.")
                continue

            target_row, target_col, max_count = valid_moves[move_index]

            if max_count > 1:
                count_str = input(f"Enter number of rocks to move (1-{max_count}): ")
                try:
                    count = int(count_str)
                    if not (1 <= count <= max_count):
                        print(f"Invalid count. Please enter a number between 1 and {max_count}.")
                        continue
                except ValueError:
                    print("Invalid number. Please try again.")
                    continue
            else:
                count = 1

            controller.move_rocks(target_row, target_col, count)
        except ValueError:
            print("Invalid input. Please try again.")


def active_player_places_rock(controller):
    while True:
        position_str = input("Enter position to place a rock (row,col): ")
        position = parse_position(position_str)

        if position is None:
            print("Invalid position format. Please use 'row,col'.")
            continue

        row, col = position

        try:
            if controller.place_rock(row, col):
                break
            else:
                print("Invalid position. Please try again.")
        except IndexError:
            print("Position is outside the board. Please try again.")


if __name__ == "__main__":
    main()