
def innerFunc():

    def inner():
        print("Hello")

    return inner()

innerFunc()