

class XoTool(object):

    def __init__(self, is_x):
        self.x_color = (255, 0, 0)
    
    def draw(self):
        pygame.draw.ellipse(s, self.color (x - 4, y - 4, 8, 8))
    
    
    
class XoGame(object):
    GRID_SIZE = 3

    def __init__(self, grid_size=32):

        self.screen = pygame.Surface((grid_size, grid_size))

        self.grid_color = (255, 255, 255)
        self.grid = pygame.Surface(self.screen.get_size())
        
        grid_line_widht = 1
        grid_sep = (self.grid.get_width - 2 * grid_line_widht) // self.GRID_SIZE
        
        for i in [grid_sep, grid_sep * 2]:
            pygame.draw.line(self.grid, self.grid_color, (grid_sep, 0), (grid_sep, grid_size), grid_line_widht)
            pygame.draw.line(self.grid, self.grid_color, (0, grid_sep), (grid_size, grid_sep), grid_line_widht)

        self.electrodes_map = [0, 1, 1, 2,
                               3, 4, 4, 5,
                               3, 4, 4, 5,
                               6, 7, 7, 8]

    def run(self):
        s = pygame.Surface(constants.RGB_MATRIX_SIZE)
        
        while True:
            self.electrodes.update()

            for i in self.electrodes.get_newly_touched():
                xo_index =self.electrodes_map[i.index]
                

            # self.draw.rectangle((0, 0) + constants.RGB_MATRIX_SIZE, fill=(0, 0, 0))
            # my_group.update()
            # my_group.draw(screen)
            # pygame.display.flip()
            pil_string_image = pygame.image.tostring(s, 'RGB', False)
            pil_image = Image.frombytes('RGB', s.get_size(), pil_string_image)
            self.matrix.SetImage(pil_image, 0, 0)
            time.sleep(0.01)

