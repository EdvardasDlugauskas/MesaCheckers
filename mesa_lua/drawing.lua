-- load images
local board_tile_image = love.graphics.newImage("images/board_tile_128.png")
local board_tile_highlighted_image = love.graphics.newImage("images/board_tile_highlighted_128.png")
local rock_white_image = love.graphics.newImage("images/rock_white_128.png")
local rock_black_image = love.graphics.newImage("images/rock_black_128.png")
local rock_images = {rock_white_image, rock_black_image}

drawing = {
    mx=0, my=0,
	window_width=800,
	window_height=600,
	tile_width=board_tile_image:getWidth(),
	tile_height=board_tile_image:getHeight(),
	tile_depth=10,  -- FIXME: hardcoded
	rock_depth=12,  -- FIXME: hardcoded
}

-- location of the board (top left pixel of top tile)
local abs_x = drawing.window_width/2
local abs_y = drawing.tile_height/2

drawing.ox = abs_x
drawing.oy = abs_y


function drawing.draw_current_game(game_state)
    -- calculate coordinates for each tile
    for bx=1, game_state.board.size do
        for by=1, game_state.board.size do
		    local tile_img = board_tile_image
			if game_state.valid_moves[bx] and game_state.valid_moves[bx][by] then
			    tile_img = board_tile_highlighted_image
			end
		    drawing.draw_board_tile(game_state, bx, by, tile_img)
		end
	end
end


function drawing.draw_board_tile(game_state, bx, by, tile_img)
	local x = (by - bx) * (drawing.tile_width/2) + abs_x
	local y = (bx + by) * (drawing.tile_height - drawing.tile_depth) / 2 + abs_y
	love.graphics.draw(
		tile_img, 
		x, y, 
		0,      -- rotation
		1, 1,   -- scale
		drawing.tile_width / 2, drawing.tile_height / 2   -- origin offset
	)
	-- draw pile on the tile
	if #game_state.board.piles[bx][by] then
		drawing.draw_pile(game_state.board.piles[bx][by], x, y)
	end
end


function drawing.draw_pile(pile, x, y)
    -- draw each rock in a pile, bottom->top
    for i=1, #pile.rocks do
	    local rock_img = rock_images[pile.rocks[i]]
	    drawing.draw_rock(rock_img, x, y - drawing.rock_depth * i)
    end
end


function drawing.draw_rock(rock_img, x, y)
	love.graphics.draw(
		rock_img,
		x, y,
		0,     -- rotation
		1, 1,  -- scale
		rock_img:getWidth() / 2, rock_img:getHeight() / 2   -- origin offset
	)
end


return drawing