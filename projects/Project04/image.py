from PIL import Image
i = Image.open('rabbit.png')

#1. Greyscale and similar effects, by processing pixels in place or from old to new

p = i.load()
sx, sy = i.size
for x in range(sx):
    for y in range(sy):
        r, g, b = p[x, y]
        gr = int ((r + g + b) / 3)
        p[x, y] = (gr, gr, gr)

def grey(p):
    r, g, b = p
    gr = int((r + g + b) / 3)
    return (gr, gr, gr)

def process_pixels(f, i):
    p = i.load()
    i2 = i.copy()
    p2 = i2.load()
    sx, sy = i.size
    for x in range(sx):
        for y in range(sy):
            p2[x, y] = f(p[x, y])
    return i2

gr = process_pixels(grey, i)

def process_pixels_in_place(f, i):
   p = i.load()
   sx, sy = i.size
   for x in range(sx):
       for y in range(sy):
           p[x, y] = f(p[x, y])

gr.save('greyrabbit.png')

#Qs: VFlip, HFlip, Rotate, Brightness, Contrast.

#2. make an image from scratch. Use this to do blurring by copying over the original and then processing.
n = Image.new('RGB', (500, 500))


n.save('new.png')

#3. A function to add a coloured border to an image
def border(i, width, colour):
    sx, sy = i.size
    p = i.load()
    i2 = Image.new('RGB', (sx + width * 2, sy + width * 2), colour)
    p2 = i2.load()
    for x in range(sx):
        for y in range(sy):
            p2[x + width, y + width] = p[x, y]
    return i2

#4. Use this to make the blur correct.
def blur(i):
    p = i.load()
    i2 = i.copy()
    p2 = i2.load()
    sx, sy = i.size
    for x in range(3, sx - 3):
        for y in range(3, sy - 3):
            sumr, sumg, sumb = 0, 0, 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    sourcer, sourceg, sourceb = p[x + dx, y + dy]
                    sumr = sumr + sourcer
                    sumg = sumg + sourceg
                    sumb = sumb + sourceb
            p2[x, y] = int (sumr / 9), int (sumg / 9), int (sumb / 9)
    return i2

bordered = border(i, 20, (255, 255, 255))

x = blur(blur(blur(bordered)))

x.save('blurred.png')

#Q: Animated blur out
def make_images_blur(i, n):
    image = i
    images = [i]
    for x in range(n):
        image = blur(image)
        images.append(image)
    return images

#images = make_images_blur(bordered, 20)

#images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)

#5. Animated fade out
def fadeby(f, p):
  r, g, b = p
  r_out = int ((f * r + (100 - f) * 255) / 100)
  g_out = int ((f * g + (100 - f) * 255) / 100)
  b_out = int ((f * b + (100 - f) * 255) / 100)
  return (r_out, g_out, b_out)

def make_images(i):
    images = []
    for x in range(100, -1, -5):
        print(x)
        def fade(p): return fadeby(x, p)
        faded = process_pixels(fade, i)
        images.append(faded)
    return images

images = make_images(i)

images[0].save('fade.gif', save_all=True, append_images=images[1:], duration=100, loop=0)

#for n, x in enumerate(images):
#    x.save(f'fade{n}.gif')

#Q: Animated blur out
def make_images_blur(i, n):
    image = i
    images = [i]
    for x in range(n):
        image = blur(image)
        images.append(image)
    return images

#images = make_images_blur(bordered, 20)

#images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)

#more Qs: A gif reverser, speeder upper, etc, fade back and forth

