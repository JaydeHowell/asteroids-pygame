import pygame


class AABB:
    def __init__(self, center: pygame.Vector2, half_dimension: pygame.Vector2):
        self.center = center
        self.half_dimension = half_dimension
        self.x_min: float = self.center.x - self.half_dimension.x
        self.x_max: float = self.center.x + self.half_dimension.x
        self.y_min: float = self.center.y - self.half_dimension.y
        self.y_max: float = self.center.y + self.half_dimension.y


class QuadtreeNode:
    
    CAPACITY = 4

    def __init__(self, boundary: AABB):
        self.boundary = boundary
        self.items = []
        self.divided = False

        # children[0] = Northwest
        # children[1] = Northeast
        # children[2] = Southwest
        # children[3] = Southeast
        self.children = [None, None, None, None]


    def insert(self, item) -> bool:
        if item.position.x == 0:
            return False

        if self.divided == False:
            if len(self.objects) < QuadtreeNode.CAPACITY:
                self.items.append(item)
                return True
            
            self.subdivide()

        if self.children[0].insert(item): return True


    def subdivide(self):
        new_half_dimension = pygame.Vector2(self.half_dimension.x / 2, self.half_dimension.y / 2)
        nw_center = pygame.Vector2(self.boundary.center.x - new_half_dimension.x, self.boundary.center.y - new_half_dimension.y)
        ne_center = pygame.Vector2(self.boundary.center.x + new_half_dimension.x, self.boundary.center.y - new_half_dimension.y)
        sw_center = pygame.Vector2(self.boundary.center.x - new_half_dimension.x, self.boundary.center.y + new_half_dimension.y)
        se_center = pygame.Vector2(self.boundary.center.x + new_half_dimension.x, self.boundary.center.y + new_half_dimension.y)

        nw_bounding = AABB(nw_center, new_half_dimension)
        nw_node = QuadtreeNode(nw_bounding)
        self.children[0] = nw_node

        ne_bounding = AABB(ne_center, new_half_dimension)
        ne_node = QuadtreeNode(ne_bounding)
        self.children[1] = ne_node

        sw_bounding = AABB(sw_center, new_half_dimension)
        sw_node = QuadtreeNode(sw_bounding)
        self.children[2] = sw_node

        se_bounding = AABB(se_center, new_half_dimension)
        se_node = QuadtreeNode(se_bounding)
        self.children[3] = se_node

        self.divided = True
