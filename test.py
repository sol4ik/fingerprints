from modules.dataset import Dataset


def test():
    # counters for result statistics
    POS_VER = 0
    POS_NONVER = 0
    NEG_VER = 0
    NEG_NONVER = 0

    for sample in range(1, 51):
        print("..", sample, "/ 50")

        name = "sub" + str(sample)

        for img in ["yes.jpg", "no.jpg"]:
            dataset = Dataset("training_data/" + name)
            dataset.load_data()
            dataset.add_new("test_data" + name + "/" + img)
            dataset.pca_calculate()
            verified = dataset.verify()

            response = ""
            if verified and img == "yes.png":
                response = "> positive verified"
                POS_VER += 1
            elif verified and img == "no.png":
                response = "! negative verified"
                NEG_VER += 1
            elif not verified and img == "yes.png":
                response = "! negative non-verified"
                NEG_NONVER += 1
            else:
                response = "> positive non-verified"
                POS_NONVER += 1
            print(response)

    print("\n\ntotal statistics:")
    print("> positive verified: ", POS_VER, "/ 25")
    print("> positive non-verified: ", POS_NONVER, "/ 25")
    print("> negative verified: ", NEG_VER, "/ 25")
    print("> negative non-verified: ", NEG_NONVER, "/ 25")


if __name__ == "__main__":
    test()
