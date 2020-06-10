import matplotlib.pyplot as plt
import numpy as np


def compute(z, thresh=4, max_steps=25):
    # Z_(n) = (Z_(n-1))^2 + c
    # Z_(0) = c
    c = z
    z = 0
    i=1
    while i<max_steps and (z*z.conjugate()).real<thresh:
        z=z ** 2 +c
        i+=1
    return i


def plotter(thresh, max_steps=25):
    scale = lambda x,y: (x / 700 * 2.47 - 2, y/500*2.24-1.12)
    img=np.full((500,700), 255)

    x_lower = 0
    x_upper = 700
    y_lower = 0
    y_upper = 500

    for x in range(x_lower, x_upper):
        for y in range(y_lower, y_upper):
            it = compute(complex(*scale(x,y)), thresh=thresh, max_steps=max_steps)
            img[y][x] = 255 - it

    return img[y_lower:y_upper, x_lower:x_upper]


img = plotter(thresh=4, max_steps=50)

plt.imshow(img, cmap="gray")
plt.axis("on")
plt.show()

