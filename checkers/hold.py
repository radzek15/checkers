from pygame.mouse import get_pos


class Hold:
    def __init__(self, surface, coords):
        self.surface = surface
        self.coords = coords
        self.rect = self.surface.get_rect()

    def place_piece(self, surf):
        mouse = get_pos()
        self.rect.x = mouse[0] + self.coords[0]
        self.rect.y = mouse[1] + self.coords[1]
        surf.blit(self.surface, self.rect)

    def collisions(self, rects):
        for rect in rects:
            if rect.colliderect(self.rect):
                return rect
        return None
