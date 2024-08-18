def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")

    return wrapper


def say_whee():
    print("Whee!")


# @decorator
def easy_say_whee():
    print("easy whee")


easy_say_whee()
