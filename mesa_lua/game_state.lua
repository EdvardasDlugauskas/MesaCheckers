local Board = require("board")


local GameState = {}


function GameState:new(board_size)
    local game_state = {
        board=Board:new(board_size),
		active_player=1,
		active_xy=nil,
		active_pile_size=0,
		valid_moves={},
		n_rocks=1,
		rock_was_left=false
    }
	
	-- TEMP
	game_state.board.piles[3][5]:add_rock(1)
	game_state.board.piles[3][5]:add_rock(1)
	game_state.board.piles[3][5]:add_rock(2)
	game_state.board.piles[2][5]:add_rock(2)
	game_state.board.piles[2][4]:add_rock(1)
	game_state.board.piles[1][1]:add_rock(2)
	game_state.board.piles[1][1]:add_rock(1)
	
    setmetatable(game_state, self)
    self.__index = self
    return game_state
end


return GameState