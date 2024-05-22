import pygame, math, time, random
from tqdm import tqdm



def rand_line(dots):
    while True:
        line = (
            random.randint(0, dots-1),
            random.randint(0, dots-1)
        )
        
        if abs(line[0] - line[1]) > 2:
            return line
        
def calc_line(line, size, dots):
    x_size, y_size = size
    x_size, y_size = x_size//2, y_size//2
        
    s,e = line
    sa = 2*math.pi*(s/dots)
    sp = (x_size+int(math.cos(sa)*x_size), y_size+int(math.sin(sa)*y_size))
    
    ea = 2*math.pi*(e/dots)
    ep = (x_size+int(math.cos(ea)*x_size), y_size+int(math.sin(ea)*y_size))
    
    length = ((sp[0] - ep[0])**2 + (sp[1] - ep[1])**2)**0.5

    return sp, ep, length

def calc_improvement(line, image, size, dots):
    sp, ep, length = calc_line(line, size, dots)

    score = 0
    for d in map(lambda n: n/length, range(int(length))):
        cp = (int(sp[0]*(1-d) + ep[0]*d), int(sp[1]*(1-d) + ep[1]*d))
        
        if not ((0 <= cp[0] < size[0]) and (0 <= cp[1] < size[1])):
            continue

        val = image.get_at(cp)[0] + image.get_at(cp)[1] + image.get_at(cp)[2]
        val /= 3

        score += 255-val

    return score/length


def draw_line(line, surface, color, thickness, size, dots, extend = False):
    sp, ep, length = calc_line(line, size, dots)

    if extend:
        d = ep[0] - sp[0], ep[1] - sp[1]
        sp = sp[0]-d[0], sp[1]-d[1]
        ep = ep[0]+d[0], ep[1]+d[1]

    pygame.draw.aaline(surface, color, sp, ep, thickness)


def render(image, surface, dots, lines, num_candidates, thickness=1, flip=True, extend=False):
    size = surface.get_size()
    image = pygame.transform.scale(image, size)
    surface.fill((255, 255, 255))

    for i in tqdm(range(lines)):
        candidates = (rand_line(dots) for i in range(num_candidates))
        line = max(candidates, key=lambda l: calc_improvement(l, image, size, dots))

        draw_line(line, surface, (0, 0, 0), thickness, size, dots, extend)
        # surface.blit(image, (0, 0))
        draw_line(line, image, (255, 255, 255, 64), thickness, size, dots)
        
        if flip:
            pygame.display.flip()
        
def main():
    pygame.init()
    dest = pygame.display.set_mode((1080, 1080))

    # dest = pygame.Surface((1080, 1080))
    image = pygame.image.load("./face.jpg")
    
    for i in range(30):
        print(f"\nRendering image {i}")
        render(image, dest,
            dots=1000,
            lines=1000,
            num_candidates=20,
            flip=True,
            extend=True)
        
        pygame.image.save(dest, f"{i:0>3}.png")

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.quit:
    #             exit()
    #     pygame.display.flip()

    # pygame.image.save(dest, f"output/{i:0>4}.png")
    



if __name__ == "__main__":
    main()
