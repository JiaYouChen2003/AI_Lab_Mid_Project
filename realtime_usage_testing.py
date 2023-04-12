from yolov3_tarot import tarot_model

import glob
import numpy as np
from PIL import Image

model = tarot_model()

images = glob.glob("./test/*.jpg")
for image in images:
    img = Image.open(image)
    img = np.array(img)
    box = model.run(img)
    print(box)