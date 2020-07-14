import interpreter


def main():
    try:
        file_name = input("Please input a file path to interpret.")
        with open(file_name, "r") as fp:
            file_text = fp.read(-1)
            interpreted_result = interpreter.main(file_text)
            print(interpreted_result)
            print("Finished Interpretation. Closing...")
    except:
        print("Incorrect file name. Closing...")


if __name__ == "__main__":
    main()
