from mesacheckers.game_state import GameState, RockColor


class ASCIIRenderer:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    def render_board(self) -> str:
        # Column headers
        result = "  " + " ".join(str(i) for i in range(self.game_state.board.size)) + "\n"
        
        # Horizontal line
        result += "  " + "-" * (2 * self.game_state.board.size - 1) + "\n"
        
        # Board rows
        for row in range(self.game_state.board.size):
            # Row header
            result += f"{row}|"
            
            # Piles in the row
            for col in range(self.game_state.board.size):
                pile = self.game_state.board.get_pile(row, col)
                
                # Render the pile
                if pile.height == 0:
                    # Empty pile
                    result += " "
                else:
                    # Pile with rocks, show the top rock
                    top_rock = pile.top_rock
                    if top_rock.color == RockColor.WHITE:
                        result += "W"
                    elif top_rock.color == RockColor.BLACK:
                        result += "B"
                    else:  # PURPLE
                        result += "P"
                
                # Add separator between piles
                if col < self.game_state.board.size - 1:
                    result += " "
            
            # End of row
            result += "\n"
        
        return result
    
    def render_pile_details(self, row: int, col: int) -> str:
        """Render the details of a specific pile.
        
        Args:
            row: The row index of the pile.
            col: The column index of the pile.
            
        Returns:
            A string representation of the pile details.
        """
        pile = self.game_state.board.get_pile(row, col)
        
        result = f"Pile at ({row}, {col}):\n"
        result += f"Height: {pile.height}\n"
        
        if pile.height == 0:
            result += "Empty pile\n"
        else:
            result += "Rocks (bottom to top):\n"
            for i, rock in enumerate(pile.rocks):
                if rock.color == RockColor.WHITE:
                    color_str = "WHITE"
                elif rock.color == RockColor.BLACK:
                    color_str = "BLACK"
                else:  # PURPLE
                    color_str = "PURPLE"
                
                result += f"{i + 1}: {color_str}\n"
        
        return result
    
    def render_game_status(self) -> str:
        """Render the current game status.
        
        Returns:
            A string representation of the game status.
        """
        current_player = self.game_state.current_player
        
        result = "Game Status:\n"
        
        # Current player
        if current_player.color == RockColor.WHITE:
            result += "Current player: WHITE\n"
        else:
            result += "Current player: BLACK\n"
        
        # Active pile
        if self.game_state.active_pile_position is not None:
            active_row, active_col = self.game_state.active_pile_position
            result += f"Active pile: ({active_row}, {active_col})\n"
        else:
            result += "Active pile: None\n"
        
        # Turn status
        if self.game_state.turn_complete:
            result += "Turn status: Complete (end turn to continue)\n"
        else:
            result += "Turn status: In progress\n"
        
        # Check win condition
        if self.game_state.check_win_condition(current_player):
            result += "GAME OVER: Current player has won!\n"
        
        return result
    
    def render_full_game(self) -> str:
        """Render the full game state.
        
        Returns:
            A string representation of the full game state.
        """
        return (
            self.render_game_status() + "\n" +
            self.render_board()
        )