import os

from image import Image

DATA_DIR = "../../data"
TO_SAVE_DIR ="../../training_data/"
SAMPLE_DIR = "sub"


def crop_train_data():
    i = 0
    for subdir in os.walk(DATA_DIR):
        for sample in os.walk(subdir[0]):
            i += 1
            for img in os.listdir(sample[0]):
                print(sample[0] + "/" + img)
                new_img = Image(sample[0] + "/" + img)
                new_img.crop_image()
                # new_img.save_img(TO_SAVE_DIR + "/" + SAMPLE_DIR + str(i) + "/" + img)
        return

crop_train_data()
