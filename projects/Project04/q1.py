from PIL import Image
i = Image.open('rabbit.png')

#Question 1
#Write functions to increase or decrease the brightness and contrast of an image. Brightness may be achieved by simple addition of each component of each pixel by an appropriate factor, and contrast by multiplication.
def brightness(p, x):
  r, g, b = p
  r_out = r
  g_out = g
  b_out = b
  return (r_out, g_out, b_out)

def contrast(p, x):
  r, g, b = p
  r_out = r
  g_out = g
  b_out = b
  return (r_out, g_out, b_out)

def process_pixels(f, i):
    p = i.load()
    i2 = i.copy()
    p2 = i2.load()
    sx, sy = i.size
    for x in range(sx):
        for y in range(sy):
            p2[x, y] = f(p[x, y])
    return i2

def brightness_image(i, x):
    def b(p): return brightness(p, x)
    return process_pixels(b, i)

def contrast_image(i, x):
    def c(p): return contrast(p, x)
    return process_pixels(c, i)

bright = brightness_image(i, 1.5)
dim = brightness_image(i, 0.5)
low_contrast = contrast_image(i, 0.5)
high_contrast = contrast_image(i, 1.5)

bright.save('bright.png')
dim.save('dim.png')
low_contrast.save('low_contrast.png')
high_contrast.save('high_contrast.png')

