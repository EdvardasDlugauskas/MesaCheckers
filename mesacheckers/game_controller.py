from typing import Tuple, List

from mesacheckers.game_state import GameState, Rock


class GameController:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    def place_rock(self, row: int, col: int) -> bool:
        """Place a rock of the current player's color on the specified pile.
        
        Args:
            row: The row index of the pile.
            col: The column index of the pile.
            
        Returns:
            True if the rock was successfully placed, else False.
        """
        # -------------
        # Validation
        # -------------

        # turn is still active
        if self.game_state.turn_complete:
            return False
        
        pile = self.game_state.board.get_pile(row, col)
        
        # pile height limit
        if pile.height >= 4:
            return False
        
        # cannot place on opponent's rock
        top_rock = pile.top_rock
        if top_rock is not None and top_rock.color != self.game_state.current_player.color:
            return False

        # -------------
        # Action
        # -------------

        rock = Rock(self.game_state.current_player.color)
        pile.add_rock(rock)
        
        self.game_state.active_pile_position = (row, col)
        
        return True
    
    def move_rocks(self, target_row: int, target_col: int, count: int) -> bool:
        """Move rocks from the active pile to the target pile.
        
        Args:
            target_row: The row index of the target pile.
            target_col: The column index of the target pile.
            count: The number of rocks to move.
            
        Returns:
            True if the rocks were successfully moved, else False.
        """
        # -------------
        # Validation
        # -------------

        # there must be an active pile
        if self.game_state.active_pile_position is None:
            return False
        
        active_row, active_col = self.game_state.active_pile_position
        active_pile = self.game_state.board.get_pile(active_row, active_col)
        target_pile = self.game_state.board.get_pile(target_row, target_col)
        
        # move is orthogonal
        if not self.game_state.board.are_positions_orthogonal(
            (active_row, active_col), (target_row, target_col)
        ):
            return False
        
        # active pile has enough rocks
        if active_pile.height < count:
            return False
        
        # selected rocks are of current player's color
        rocks_to_check = active_pile.rocks[-count:]
        player_color = self.game_state.current_player.color
        
        if not all(rock.color == player_color for rock in rocks_to_check):
            return False
        
        # target pile's height is less than the lowest selected rock
        lowest_selected_rock_height = active_pile.height - count + 1
        if target_pile.height >= lowest_selected_rock_height:
            return False

        # -------------
        # Action
        # -------------

        # Move the rocks
        rocks_to_move = active_pile.remove_rocks(count)
        for rock in rocks_to_move:
            target_pile.add_rock(rock)

        can_move_again = active_pile.top_rock is not None and active_pile.top_rock.color == player_color
        if can_move_again:
            self.game_state.active_pile_position = (target_row, target_col)
        else:
            self.game_state.turn_complete = True
        
        return True
    
    def end_turn(self) -> None:
        """End the current player's turn and move to the next player."""
        # Check if the current player has won
        if self.game_state.check_win_condition(self.game_state.current_player):
            # Game is over, current player has won
            # This could trigger some game-over logic
            pass
        else:
            # Move to the next player's turn
            self.game_state.next_turn()
    
    def get_valid_moves(self) -> List[Tuple[int, int, int]]:
        """Get a list of valid moves from the active pile.
        
        Returns:
            A list of tuples (row, col, max_count) representing valid target positions
            and the maximum number of rocks that can be moved there.
        """
        if self.game_state.active_pile_position is None:
            return []
        
        active_row, active_col = self.game_state.active_pile_position
        active_pile = self.game_state.board.get_pile(active_row, active_col)
        player_color = self.game_state.current_player.color
        
        # consecutive rocks from top
        consecutive_count = 0
        for rock in reversed(active_pile.rocks):
            if rock.color == player_color:
                consecutive_count += 1
            else:
                break
        
        if consecutive_count == 0:
            return []
        
        valid_moves = []
        
        # orthogonal positions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            target_row, target_col = active_row + dr, active_col + dc
            
            # board bounds check
            if not (0 <= target_row < self.game_state.board.size and 0 <= target_col < self.game_state.board.size):
                continue
            
            target_pile = self.game_state.board.get_pile(target_row, target_col)
            
            # check how many rocks can be moved
            max_count = 0
            for i in range(1, consecutive_count + 1):
                lowest_selected_rock_height = active_pile.height - i + 1
                if target_pile.height < lowest_selected_rock_height:
                    max_count = i
                else:
                    break
            
            if max_count > 0:
                valid_moves.append((target_row, target_col, max_count))
        
        return valid_moves