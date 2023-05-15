import os

def change_directory(target_path, callback):
    """
    Change the current directory to a specified target path.

    If the target path doesn't exist, prompt the user (once) to recursively go back and change to a valid path.

    Returns:
        True if the change of directory was successful.
    """
    response_flag = False
    while not os.path.isdir(target_path) and target_path != "/":
        if not response_flag:
            # response = input("Path not found. Do you want to go one directory back? (y/n): ")
            # response = self.ask_yesno("Path not found. Do you want to go one directory back?")
            response = callback("Path not found. Do you want to go one directory back?")
            # self.log.info("response self " + response)
        if response == "yes":
            # Move one directory back
            target_path = os.path.dirname(target_path)
            response_flag = True
        else:
            return False

    if target_path != "/":
        os.chdir(target_path)
        print("Changed directory to:", os.getcwd())
    else:
        print("Path does not exist")

    return True