def save_imageP3(nCols, nRows, file_name, lo_pixels):
    """
    Takes in
    Outputs a PPM image file in P3 format - a text file containing:
    =================
    P3
    nCols nRows
    max_color_val
    r1 g1 b1
    r2 g2 b2
    ...
    rn gn bn
    =================
    """
    max_color_val = 255

    print(f"Saving image {file_name}: {nCols} x {nRows}\n")

    fp = open(file_name, "w")
    if not fp:
        print(f"Unable to open file '{file_name}'\n")
        return

    fp.write(f"P3\n")
    fp.write(f"{nCols} {nRows}\n")
    fp.write(f"{max_color_val}\n")

    for x in range(nRows):
        for y in range(nCols):
            fp.write(
                f" {lo_pixels[x][y][0]} {lo_pixels[x][y][1]} {lo_pixels[x][y][2]}")
        fp.write("\n")
    fp.close()
