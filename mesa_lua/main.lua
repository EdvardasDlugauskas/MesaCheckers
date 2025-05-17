local Drawing = require("drawing")
local GameState = require("game_state")
local GameController = require("game_controller")
local Board = require("board")


function love.load()	
	game_state = GameState:new(6)  -- or load from save
	GameController.get_valid_starting_moves(game_state)
end


function love.update()
	capture_mouse_position()
end


function love.draw()
    Drawing.draw_current_game(game_state)
end


function love.keypressed(key)
    GameController.resolve_keypress(key, game_state)
end


function capture_mouse_position()
	Drawing.mx, Drawing.my = love.mouse.getX(), love.mouse.getY()
	
	if love.mouse.isDown(1) then	
		local by = math.floor(((Drawing.mx - Drawing.ox) / (Drawing.tile_width/2 ) +
		                       (Drawing.my - Drawing.oy) / (Drawing.tile_height/2)) / 2) + 1
	    local bx = math.floor(((Drawing.my - Drawing.oy) / (Drawing.tile_height/2) -
		                       (Drawing.mx - Drawing.ox) / (Drawing.tile_width/2 )) / 2) + 1
        GameController.resolve_click(bx, by, game_state)
    end
end
