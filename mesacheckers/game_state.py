from enum import Enum, auto
from typing import Optional, List, Tuple


class RockColor(Enum):
    WHITE = auto()
    BLACK = auto()
    PURPLE = auto()  # Optional color for marking piles of height 4


class Rock:
    """Represents a single rock in the game."""
    
    def __init__(self, color: RockColor):
        self.color = color
    
    def __repr__(self) -> str:
        return f"Rock({self.color.name})"


class Pile:
    """Represents a pile of rocks on the board."""
    
    def __init__(self):
        self.rocks: List[Rock] = []
    
    @property
    def height(self) -> int:
        return len(self.rocks)
    
    @property
    def top_rock(self) -> Optional[Rock]:
        """Get the top rock of the pile, or None if the pile is empty."""
        if not self.rocks:
            return None
        return self.rocks[-1]
    
    def add_rock(self, rock: Rock) -> None:
        """Add a rock to the top of the pile."""
        self.rocks.append(rock)
    
    def remove_rocks(self, count: int) -> List[Rock]:
        """Remove and return the specified number of rocks from the top of the pile.
        
        Args:
            count: The number of rocks to remove.
            
        Returns:
            The removed rocks, with the topmost rock at the end of the list.
        """
        if count > self.height:
            raise ValueError(f"Cannot remove {count} rocks from a pile of height {self.height}")
        
        removed_rocks = self.rocks[-count:]
        self.rocks = self.rocks[:-count]
        return removed_rocks
    
    def __repr__(self) -> str:
        return f"Pile(rocks={self.rocks})"


class Board:
    def __init__(self):
        self.size = 6
        self.piles = [[Pile() for _ in range(self.size)] for _ in range(self.size)]
    
    def get_pile(self, row: int, col: int) -> Pile:
        """Get the pile at the specified position.
        
        Args:
            row: The row index (0-5).
            col: The column index (0-5).
            
        Returns:
            The pile at the specified position.
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Position ({row}, {col}) is outside the board")
        
        return self.piles[row][col]
    
    def get_corner_piles(self) -> List[Pile]:
        """Get the four corner piles of the board."""
        return [
            self.piles[0][0],  # Top-left
            self.piles[0][self.size - 1],  # Top-right
            self.piles[self.size - 1][0],  # Bottom-left
            self.piles[self.size - 1][self.size - 1],  # Bottom-right
        ]
    
    def are_positions_orthogonal(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """Check if two positions are orthogonally adjacent.
        
        Args:
            pos1: The first position (row, col).
            pos2: The second position (row, col).
            
        Returns:
            True if the positions are orthogonally adjacent, else False.
        """
        row1, col1 = pos1
        row2, col2 = pos2
        
        # Check if positions are the same
        if row1 == row2 and col1 == col2:
            return False
        
        # Check if positions are orthogonally adjacent
        return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1)


class Player:
    def __init__(self, color: RockColor):
        self.color = color
    
    def __repr__(self) -> str:
        return f"Player({self.color.name})"


class GameState:
    def __init__(self, first_player_color: RockColor = RockColor.WHITE):
        self.board = Board()
        self.players = [
            Player(first_player_color),
            Player(RockColor.BLACK if first_player_color == RockColor.WHITE else RockColor.WHITE)
        ]
        self.current_player_index = 0
        self.active_pile_position: Optional[Tuple[int, int]] = None
        self.turn_complete = False
    
    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]
    
    def next_turn(self) -> None:
        """Move to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.active_pile_position = None
        self.turn_complete = False
    
    def check_win_condition(self, player: Player) -> bool:
        """Check if the specified player has won.
        
        A player wins if each of the 4 corner piles either has a height of 4 or
        has a rock of the player's color on top.
        
        Args:
            player: The player to check for a win.
            
        Returns:
            True if the player has won, else False.
        """
        for pile in self.board.get_corner_piles():
            if pile.height == 4:
                continue

            top_rock = pile.top_rock
            if top_rock is None or top_rock.color != player.color:
                return False
        
        return True