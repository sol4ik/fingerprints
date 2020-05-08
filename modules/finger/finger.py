class Finder:
    def __init__(self, name, type="index"):
        """
        :param name: id of sample from dataset / name of person for custom usage
        :param type: finger type: thumb, index, middle, ring, pinky
        """
        self.name = name
        self.type = type
        self.pictures = list()
