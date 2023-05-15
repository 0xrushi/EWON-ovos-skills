def convert_to_path(input_string):
    """
    returns a path from the requested cd command
    
    "can you cd to slash home slash bread slash dot config slash o-boss" -> /home/bread/.config/o-boss

    """
    # Find the index of the first slash
    first_slash_index = input_string.find("slash")
    # Extract the substring starting from the first slash
    path = input_string[first_slash_index:]
    path = path.replace("slash", "/")
    path = path.replace("dot", ".")
    path = path.strip("/")
    path = path.replace(" ", "")
    return "/" + path