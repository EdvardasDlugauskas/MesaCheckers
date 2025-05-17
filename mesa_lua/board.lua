local Pile = require("pile")

Board = {}

function Board:new(size)
    local board = {
        size=size,
        piles={}
    }

    for x=1, size do
        board.piles[x] = {}
        for y=1, size do
            board.piles[x][y] = Pile:new()
        end
    end

    setmetatable(board, self)
    self.__index = self
    return board
end

return Board