import logger
import oled
import buttons
import sprites

class Tile:
    def __init__(self, x_anchor, y_offset, width, height, title, callback=None):
        self.x_anchor = x_anchor
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.selected = 0
        self.state = 0
        self.callback = callback

    def on_select(self, selected=None):
        if selected is None:
            return self.selected
        if selected is not None:
            selected_y_offset = self.y_offset + self.height + 4
            oled.display.fill_rect(self.x_anchor + 4, selected_y_offset, self.width - 8, 3, selected)
            oled.display.show()
        
    def draw(self, state=None):
        if state is None:
            return self.state
        self.callback(self.x_anchor, self.y_offset, state)
        self.state = state
        
    def deselect(self):
        self.selected = 0

class Menu:
    def __init__(self, tiles):
        if not 1 <= len(tiles) <= 3:
            raise ValueError("Menu must have between 1 and 3 tiles.")
        self.tiles = tiles
        self.selected_tile = 0

    # Select a tile and call its callback
    def select(self, index):
        if index < 0 or index >= len(self.tiles):
            raise IndexError("Invalid tile index.")
        
        # Deselect all tiles
        for tile in self.tiles:
            tile.on_select(0)
        
        self.selected_tile = index
        self.tiles[index].on_select(1)

    # Get the currently selected tile
    def selected(self):
        return self.selected_tile

    # Getter and Setter for the first tile's state
    def first(self, state=None):
        if state is None:
            return self.tiles[0].state
        self.tiles[0].state = state
        self.tiles[0].draw(state)

    # Getter and Setter for the second tile's state
    def second(self, state=None):
        if len(self.tiles) < 2:
            raise IndexError("Second tile is not defined.")
        if state is None:
            return self.tiles[1].state
        self.tiles[1].state = state
        self.tiles[1].draw(state)

    # Getter and Setter for the third tile's state
    def third(self, state=None):
        if len(self.tiles) < 3:
            raise IndexError("Third tile is not defined.")
        if state is None:
            return self.tiles[2].state
        self.tiles[2].state = state
        self.tiles[2].draw(state)

#-------------------------EXISTING-CODE-------------------------#
#-------------------------EXISTING-CODE-------------------------#

current_tile = 1
dimensions = {
    'width'      : 32,
    'height'     : 32,
    'y_offset'   : 20,
    'x_anchor_1' : 6,
    'x_anchor_2' : 48,
    'x_anchor_3' : 90,
}


config = {
    'w': 32,
    'h': 36,
    'hp': 3,
    'vp': 5
}

items = {
    "1" : "Wifi Info",
    "2" : "Wardriving",
    "3" : "Spectrum"
    }

def select_tile_next(state, config):
    """Move to the next tile, wrapping around from 3 back to 1."""
    global current_tile
    logger.write("main_menu: Selecting next tile...")
    current_tile = current_tile + 1 if current_tile < 3 else 1
    clear_title()
    display.text(menu.items[str(current_tile)], 32, 3, 1)
    logger.write("main_menu: Writing tile title.")
    display.show()
    tile(current_tile, 2, **config)

def select_tile_previous(state, config):
    """Move to the previous tile, wrapping around from 1 back to 3."""
    global current_tile
    logger.write("main_menu: Selecting previous tile...")
    current_tile = current_tile - 1 if current_tile > 1 else 3
    clear_title()
    display.text(menu.items[str(current_tile)], 32, 3, 1)
    logger.write("main_menu: Writing tile title.")
    display.show()
    tile(current_tile, 2, **config)

state = 1

dimensions = {
    'width'      : 32,
    'height'     : 32,
    'y_offset'   : 20,
    'x_anchor_1' : 6,
    'x_anchor_2' : 48,
    'x_anchor_3' : 90
}


tile_2 = ( dimensions['x_anchor_2'], dimensions['y_offset'], dimensions['width'], dimensions['height'], state )
tile_3 = ( dimensions['x_anchor_3'], dimensions['y_offset'], dimensions['width'], dimensions['height'], state )

def tile_1(state=0):
    global dimensions
    
    dims = [dimensions['x_anchor_1'], dimensions['y_offset'], dimensions['width'], dimensions['height']]
    select_dims = [dims[0], dims[1] + dims[3] + 4, dims[2]]
    
    if state == 0 or state == 1:
        oled.display.rect( dims[0], dims[1], dims[2], dims[3], state )
        
    elif state == 2:
        oled.display.fill_rect(dims[0], dims[1] + dims[3] + 2, 128, 64, 0)
        oled.display.rect( dims[0], dims[1], dims[2], dims[3], 1 )
        oled.display.fill_rect(dims[0], dims[1] + dims[3] + 4, dims[2], 3, 1)



def tile(pos, state, w, h, hp, vp):
    """
    Draw up to 3 tiles (pos = 1,2,3). 
    If pos=0, clear everything and redraw all 3 tiles in the given state.
    
    state=1 or state=0 typically means 'unselected' or 'off', 
    state=2 means 'selected' or 'highlighted'.
    """
    logger.write("main_menu: Drawing tile at pos " + str(pos) + " with state " + str(state))
    global current_tile
    # Offsets / geometry
    head_offset = 16
    tile_width  = w
    tile_height = h
    
    # Normal (outer) padding
    h_pad = hp
    v_pad = vp
    
    # "Selected" (inner) padding
    s_h_pad = hp + 3
    s_v_pad = vp + 3
    
    # Calculate anchors for each of the 3 tiles
    # x_anchor_i = left X of tile i, s_x_anchor_i = left X of small highlight border
    x_anchor_1    = 6 + h_pad
    s_x_anchor_1  = 6 + s_h_pad
    x_anchor_2    = x_anchor_1 + tile_width + (h_pad * 2)
    s_x_anchor_2  = s_x_anchor_1 + (tile_width - 6) + (s_h_pad * 2)
    x_anchor_3    = x_anchor_2 + tile_width + (h_pad * 2)
    s_x_anchor_3  = s_x_anchor_2 + (tile_width - 6) + (s_h_pad * 2)
    
    # y_anchor_top/bot for the outer border
    y_anchor_top  = head_offset + v_pad
    y_anchor_bot  = y_anchor_top + tile_height
    
    # y_anchor_top/bot for the highlight (inner) border
    s_y_anchor_top = head_offset + s_v_pad
    s_y_anchor_bot = s_y_anchor_top + (tile_height - 6)
    
    # Put them into lists for easy iteration
    outer_anchors = [
        (x_anchor_1, y_anchor_top),
        (x_anchor_2, y_anchor_top),
        (x_anchor_3, y_anchor_top),
    ]
    inner_anchors = [
        (s_x_anchor_1, s_y_anchor_top),
        (s_x_anchor_2, s_y_anchor_top),
        (s_x_anchor_3, s_y_anchor_top),
    ]
    
    if pos == 0:
        clear_body()
    
    def draw_outer_rect(x, y, w, h, st):
        display.hline(x,     y,     w, st)       # top
        display.hline(x,     y + h, w, st)       # bottom
        display.vline(x,     y,     h, st)       # left
        display.vline(x + w, y,     h, st)       # right

    def draw_inner_rect(x, y, w, h, st):
        display.hline(x,     y,     w, st)
        display.hline(x,     y + h, w, st)
        display.vline(x,     y,     h, st)
        display.vline(x + w, y,     h, st)

    # Loop over tiles 1..3
    for i in range(3):
        tile_index = i + 1
        # Coordinates for the outer border
        ox, oy = outer_anchors[i]
        # Coordinates for the inner "highlight" border
        sx, sy = inner_anchors[i]
        
        if i == 0:
            sprites.show_wifi_info_tile(sx, sy)
        
        if i == 1:
            sprites.show_wardriving_tile(sx, sy)
        
        if pos == tile_index or pos == 0:
            draw_outer_rect(ox, oy, tile_width, tile_height, state)
            
            if state == 2 and pos == tile_index:
                draw_inner_rect(sx, sy, tile_width - 6, tile_height - 6, 1)
                current_tile = tile_index
            else:
                draw_inner_rect(sx, sy, tile_width - 6, tile_height - 6, 0)
        else:
            draw_inner_rect(sx, sy, tile_width - 6, tile_height - 6, 0)
    
    display.show()


current_tile = 1

config = {
    'w': 32,
    'h': 36,
    'hp': 3,
    'vp': 5
}

items = {
    "1" : "Wifi Info",
    "2" : "Wardriving",
    "3" : "Spectrum"
    }

def select_tile_next(state, config):
    global current_tile
    logger.write("main_menu: Selecting next tile...")
    current_tile = current_tile + 1 if current_tile < 3 else 1
    clear_title()
    display.text(menu.items[str(current_tile)], 32, 3, 1)
    logger.write("main_menu: Writing tile title.")
    display.show()
    tile(current_tile, 2, **config)

def select_tile_previous(state, config):
    global current_tile
    logger.write("main_menu: Selecting previous tile...")
    current_tile = current_tile - 1 if current_tile > 1 else 3
    clear_title()
    display.text(menu.items[str(current_tile)], 32, 3, 1)
    logger.write("main_menu: Writing tile title.")
    display.show()
    tile(current_tile, 2, **config)

state = 1

dimensions = {
    'width'      : 32,
    'height'     : 32,
    'y_offset'   : 20,
    'x_anchor_1' : 6,
    'x_anchor_2' : 48,
    'x_anchor_3' : 90
}


tile_2 = ( dimensions['x_anchor_2'], dimensions['y_offset'], dimensions['width'], dimensions['height'], state )
tile_3 = ( dimensions['x_anchor_3'], dimensions['y_offset'], dimensions['width'], dimensions['height'], state )

def tile_1(state=0):
    global dimensions
    
    dims = [dimensions['x_anchor_1'], dimensions['y_offset'], dimensions['width'], dimensions['height']]
    select_dims = [dims[0], dims[1] + dims[3] + 4, dims[2]]
    
    if state == 0 or state == 1:
        oled.display.rect( dims[0], dims[1], dims[2], dims[3], state )
        
    elif state == 2:
        oled.display.fill_rect(dims[0], dims[1] + dims[3] + 2, 128, 64, 0)
        oled.display.rect( dims[0], dims[1], dims[2], dims[3], 1 )
        oled.display.fill_rect(dims[0], dims[1] + dims[3] + 4, dims[2], 3, 1)



def tile(pos, state, w, h, hp, vp):
    logger.write("main_menu: Drawing tile at pos " + str(pos) + " with state " + str(state))
    global current_tile
    # Offsets / geometry
    head_offset = 16
    tile_width  = w
    tile_height = h
    
    # Normal (outer) padding
    h_pad = hp
    v_pad = vp
    
    # "Selected" (inner) padding
    s_h_pad = hp + 3
    s_v_pad = vp + 3
    
    # Calculate anchors for each of the 3 tiles
    # x_anchor_i = left X of tile i, s_x_anchor_i = left X of small highlight border
    x_anchor_1    = 6 + h_pad
    s_x_anchor_1  = 6 + s_h_pad
    x_anchor_2    = x_anchor_1 + tile_width + (h_pad * 2)
    s_x_anchor_2  = s_x_anchor_1 + (tile_width - 6) + (s_h_pad * 2)
    x_anchor_3    = x_anchor_2 + tile_width + (h_pad * 2)
    s_x_anchor_3  = s_x_anchor_2 + (tile_width - 6) + (s_h_pad * 2)
    
    # y_anchor_top/bot for the outer border
    y_anchor_top  = head_offset + v_pad
    y_anchor_bot  = y_anchor_top + tile_height
    
    # y_anchor_top/bot for the highlight (inner) border
    s_y_anchor_top = head_offset + s_v_pad
    s_y_anchor_bot = s_y_anchor_top + (tile_height - 6)
    
    # Put them into lists for easy iteration
    outer_anchors = [
        (x_anchor_1, y_anchor_top),
        (x_anchor_2, y_anchor_top),
        (x_anchor_3, y_anchor_top),
    ]
    inner_anchors = [
        (s_x_anchor_1, s_y_anchor_top),
        (s_x_anchor_2, s_y_anchor_top),
        (s_x_anchor_3, s_y_anchor_top),
    ]
    
    if pos == 0:
        clear_body()
    
    def draw_outer_rect(x, y, w, h, st):
        display.hline(x,     y,     w, st)       # top
        display.hline(x,     y + h, w, st)       # bottom
        display.vline(x,     y,     h, st)       # left
        display.vline(x + w, y,     h, st)       # right

    def draw_inner_rect(x, y, w, h, st):
        display.hline(x,     y,     w, st)
        display.hline(x,     y + h, w, st)
        display.vline(x,     y,     h, st)
        display.vline(x + w, y,     h, st)

    # Loop over tiles 1..3
    for i in range(3):
        tile_index = i + 1
        # Coordinates for the outer border
        ox, oy = outer_anchors[i]
        # Coordinates for the inner "highlight" border
        sx, sy = inner_anchors[i]
        
        if i == 0:
            sprites.show_wifi_info_tile(sx, sy)
        
        if i == 1:
            sprites.show_wardriving_tile(sx, sy)
        
        if pos == tile_index or pos == 0:
            draw_outer_rect(ox, oy, tile_width, tile_height, state)
            
            if state == 2 and pos == tile_index:
                draw_inner_rect(sx, sy, tile_width - 6, tile_height - 6, 1)
                current_tile = tile_index
            else:
                draw_inner_rect(sx, sy, tile_width - 6, tile_height - 6, 0)
        else:
            draw_inner_rect(sx, sy, tile_width - 6, tile_height - 6, 0)
    
    display.show()