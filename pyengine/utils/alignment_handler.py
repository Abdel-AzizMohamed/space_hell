"""Contains functions to help with alignment"""
###### Python Packages ######
###### My Packages ######
#### Type Hinting ####


def align_offset(src_object: tuple, dest_object: tuple, align: str) -> tuple:
    """
    Calculate the needed offset for src_object
    to be aligned to the dest_object in the given direction

    Arguments:
        src_object: source object size
        dest_object: destination object size
        align: alignment direction

    Returns:
        A tuple contains the (x, y) alignment offset
    """
    x_offset = 0
    y_offset = 0

    x_src_size = src_object[0]
    y_src_size = src_object[1]
    half_x_src_size = src_object[0] // 2
    half_y_src_size = src_object[1] // 2

    x_dest_size = dest_object[0]
    y_dest_size = dest_object[1]
    half_x_dest_size = dest_object[0] // 2
    half_y_dest_size = dest_object[1] // 2

    if align == "top":
        x_offset = abs(half_x_src_size - half_x_dest_size)
        y_offset = 0
    if align == "topleft":
        x_offset = 0
        y_offset = 0
    if align == "topright":
        x_offset = abs(x_dest_size - x_src_size)
        y_offset = 0

    if align == "bottom":
        x_offset = abs(half_x_src_size - half_x_dest_size)
        y_offset = abs(y_src_size - y_dest_size)
    if align == "bottomleft":
        x_offset = 0
        y_offset = abs(y_src_size - y_dest_size)
    if align == "bottomright":
        x_offset = abs(x_src_size - x_dest_size)
        y_offset = abs(y_src_size - y_dest_size)

    if align == "center":
        x_offset = abs(half_x_src_size - half_x_dest_size)
        y_offset = abs(half_y_src_size - half_y_dest_size)
    if align == "midleft":
        x_offset = 0
        y_offset = abs(half_y_src_size - half_y_dest_size)
    if align == "midright":
        x_offset = abs(x_src_size - x_dest_size)
        y_offset = abs(half_y_src_size - half_y_dest_size)

    return (x_offset, y_offset)
