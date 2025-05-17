Pile = {}


function reverse_arr(arr)
    local i, j = 1, #arr
    while i < j do
        arr[i], arr[j] = arr[j], arr[i]
        i = i + 1
        j = j - 1
    end
end


function Pile:new()
    local pile = {
        rocks={},
		top_rock=nil,
		height=0,
		is_closed=false
    }
    setmetatable(pile, self)
    self.__index = self
    return pile
end


function Pile.add_rock(pile, rock)
    assert(not pile.is_closed, "pile already reached maximum height")
    table.insert(pile.rocks, rock)
	pile.top_rock = rock
	pile.height = #pile.rocks
	if pile.height == 4 then pile.is_closed = true end
end


function Pile.remove_rock(pile)  -- does not check color
    assert(#pile.rocks > 0, "no rocks to remove")
    table.remove(pile.rocks)
	pile.top_rock = pile.rocks[#pile.rocks]
	pile.height = #pile.rocks
end


function Pile.get_consecutive_color_count(pile, color)
    local count = 0
	for i=1, pile.height do
	    if pile.rocks[pile.height-i+1] == color then
		    count = count + 1
		else
		    return count
		end
	end
	return count
end


return Pile