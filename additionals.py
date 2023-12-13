def totp_text_to_dict():
    from data import secret_datas
    blocks = secret_datas.strip().split("\n\n")

    str_array = []

    # Process each block
    for block in blocks:
        # Split the block into lines
        lines = block.split("\n")
        # Extract the values from each line and add them to the array
        str_array.append([line.split(":")[1].strip() for line in lines])

    return str_array