from helpers import get_input
import pygame


class Point(object):

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def step(self, n=1):
        self.x += n*self.vx
        self.y += n*self.vy

    @classmethod
    def from_string(cls, s):
        bits = [t.split('>') for t in s.split('<')]
        pos, speed = bits[1][0], bits[2][0]
        x, y = map(int, pos.split(','))
        vx, vy = map(int, speed.split(','))
        return cls(x, y, vx, vy)

# 10,500 - 11,000

def draw(points):
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)

    minx = min(p.x for p in points)
    maxx = max(p.x for p in points)
    miny = min(p.y for p in points)
    maxy = max(p.y for p in points)

    # Set the height and width of the screen
    size = [800, 600]
    screen = pygame.display.set_mode(size)

    def scale(p):
        x = int(round(float(size[0]) * (p.x - minx)/(maxx-minx)))
        y = int(round(float(size[1]) * (p.y - miny)/(maxy-miny)))
        return x,y

    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(2)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        screen.fill(WHITE)

        # Draw a rectangle outline
        for point in points:
            x, y = scale(point)
            pygame.draw.rect(screen, BLACK, [x, y, 2, 2])

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

        raw_input()

        for point in points:
            point.step()

    # Be IDLE friendly
    pygame.quit()

def part1():
    inputs = get_input(10)#, 'test')
    points = [Point.from_string(item) for item in inputs]
    [p.step(10870) for p in points]
    draw(points)

def main():
    part1()


if __name__ == '__main__':
    main()
