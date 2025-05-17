local GameController = {}


local orth_pos = {
    {x=0, y= 1}, {x= 1, y=0},
	{x=0, y=-1}, {x=-1, y=0},
}


function GameController.resolve_click(bx, by, game_state)
	if game_state.valid_moves[bx] and game_state.valid_moves[bx][by] then
		if game_state.active_xy == nil then
		    start_new_move(bx, by, game_state)
		else
		    continue_move(bx, by, game_state)
		end
		game_state.active_xy = {x=bx, y=by}
		game_state.valid_moves = get_valid_moves(game_state)
	end
end



function start_new_move(bx, by, game_state)
    local selected_pile = game_state.board.piles[bx][by]
	selected_pile:add_rock(game_state.active_player)
end


function continue_move(bx, by, game_state)
	local active_pile = game_state.board.piles[game_state.active_xy.x][game_state.active_xy.y]
	local selected_pile = game_state.board.piles[bx][by]
	for i=1, game_state.n_rocks do
	    active_pile:remove_rock()
	    selected_pile:add_rock(game_state.active_player)
	end
end


function GameController.resolve_keypress(key, game_state)
  if (key=="return") then finish_move(game_state)
  elseif (key=="backspace") then undo_move(game_state)
  elseif (key=="1") or (key=="2") or (key=="3") or (key=="4") then select_n_rocks(key, game_state)
  end
end


function select_n_rocks(key, game_state)
    local active_pile = game_state.board.piles[game_state.active_xy.x][game_state.active_xy.y]	
    local consecutive_count = active_pile:get_consecutive_color_count(game_state.active_player)
	game_state.n_rocks = math.min(consecutive_count, tonumber(key))
end


function GameController.get_valid_starting_moves(game_state)  -- only used when there is no active pile
    local valid_moves = {}
    for bx=1, game_state.board.size do
	    valid_moves[bx] = nil
	    for by=1, game_state.board.size do
		    local pile = game_state.board.piles[bx][by]
		    if (#pile.rocks == 0)
			or ((pile.top_rock == game_state.active_player) and (not pile.is_closed)) then
				valid_moves[bx] = valid_moves[bx] or {}
				valid_moves[bx][by] = true
			end
		end
	end
	return valid_moves
end


function get_valid_moves(game_state)  -- only used when there is active pile
    local bx, by = game_state.active_xy.x, game_state.active_xy.y
	local active_pile = game_state.board.piles[bx][by]	
    -- count how many rocks can be moved
    local consecutive_count = active_pile:get_consecutive_color_count(game_state.active_player)
	if consecutive_count == 0 then return {} end
		
	local valid_moves = {}
	for i, o in ipairs(orth_pos) do
	    local target_x = bx + o.x
		local target_y = by + o.y
		-- check if outside board borders
		if (target_x < 1) or (target_x > game_state.board.size)
		or (target_y < 1) or (target_y > game_state.board.size) then do end
		else
		    local target_pile = game_state.board.piles[target_x][target_y]
		    local height_difference = active_pile.height - target_pile.height
		    if height_difference > 0 then
			    local max_move = math.min(consecutive_count, height_difference)
				valid_moves[target_x] = valid_moves[target_x] or {}
				valid_moves[target_x][target_y] = max_move
			end
		end
	end
	return valid_moves
end


--function undo_move()

function finish_move(game_state)
    if game_state.active_player == 1 then game_state.active_player = 2
	else game_state.active_player = 1 end
	game_state.active_xy = nil
	game_state.valid_moves = GameController.get_valid_starting_moves(game_state)
	game_state.n_rocks = 1
end


return GameController