from pygame.mouse import get_pos


class Hold:
    def __init__(self, surface, offset):
        self.surface = surface
        self.draw_rect = self.surface.get_rect()
        self.offset = offset

    def place_piece(self, display_surface):
        self.draw_rect.x = get_pos()[0] + self.offset[0]
        self.draw_rect.y = get_pos()[1] + self.offset[1]

        display_surface.blit(self.surface, self.draw_rect)

    def check_collision(self, rect_list):
        for rect in rect_list:
            if rect.colliderect(self.draw_rect):
                return rect

        return None
