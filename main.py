from modules.dataset import Dataset

if __name__ == "__main__":
    img_path = input("> image path ")
    owner = input("> owner's name ")

    dataset = Dataset("training_data/" + owner)
    dataset.load_data()
    dataset.add_new(img_path)
    dataset.pca_calculate()
    if dataset.verify():
        print("> verified")
    else:
        print("! not verified")
