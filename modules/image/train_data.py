import os

from image import Image

DATA_DIR = "../../data"
TO_SAVE_DIR ="../../training_data"
SAMPLE_DIR = "sub"


def crop_train_data():
    """
    Normalize and crop all the train data and save in new directory.
    """
    i = 0
    for subdir in os.walk(DATA_DIR):
        for sample in os.walk(subdir[0]):
            if sample[0] == "../../data":
                pass
            else:
                sample_dir = sample[0].strip().split("/")[-1]
                os.mkdir(TO_SAVE_DIR + "/" + sample_dir)
                for img in os.listdir(sample[0]):
                    if os.path.isfile(sample[0] + "/" + img):
                        print(sample[0] + "/" + img)
                        new_img = Image(str(sample[0] + "/" + img))
                        new_img.crop_image()
                        new_img.save_img(TO_SAVE_DIR + "/" + sample_dir + "/" + img)
        return

crop_train_data()
