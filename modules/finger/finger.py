import os

from ..image_processor import Image
from ..finger_error import FingerError


class Finger:
    def __init__(self, name, type="index", dir=''):
        """
        :param name: id of sample from dataset / name of person for custom usage
        :param type: finger type: thumb, index, middle, ring, pinky
        :param dir: directory to the pictures of fingerprints
        """
        self.name = name
        self.type = type
        self.dir = dir
        self.images = list()

    def __str__(self):
        return self.name + ": " + self.type

    def load(self):
        """
        Load all the pictures from directory given and create Image wrapper for each of them.
        """
        if self.dir == '':
            raise FingerError("no directory for fingerprint images")

        # look only for file names
        img_files = [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))]
        for img_path in img_files:
            self.images.append(Image(img_path))

    def get_images(self):
        """
        Return all the Image objects representing given Finger object.
        """
        if len(self.images) == 0:
            print("! no images uploaded for finger " + self.name + ": " + self.type)
        return self.images
