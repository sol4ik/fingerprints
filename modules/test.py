from PIL import Image
import numpy as np
from numpy import array

img = Image.open('../data/sub1/11.jpg')
ar = array(img)

ar_1channel = list()
i = -1
for row in ar:
    ar_1channel.append(list())
    i += 1
    for pixel in row:
        ar_1channel[i].append([int(sum(pixel) / 3) for _ in range(3)])

ar_1channel = np.array(ar_1channel)
print(ar_1channel)
# ar_1channel = ar_1channel.flatten()
# print(len(ar_1channel))
gr_im = Image.fromarray(ar_1channel)
gr_im.save('gr_kolala.jpg')
