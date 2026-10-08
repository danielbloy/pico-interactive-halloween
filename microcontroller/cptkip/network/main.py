from network import execute


def update() -> bool:
    return True


def trigger():
    print("trigger called")


execute(trigger, update)
