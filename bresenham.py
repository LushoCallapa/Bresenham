def get_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    if x0 < x1:
        sx = 1
    else:
        sx = -1

    if y0 < y1:
        sy = 1
    else:
        sy = -1


    if dx > dy:
        err = dx / 2.0
        while x0 != x1:
            points.append((x0, y0))
            err -= dy
            if err < 0:
                y0 += sy
                err += dx
            x0 += sx
    else:
        err = dy / 2.0
        while y0 != y1:
            points.append((x0, y0))
            err -= dx
            if err < 0:
                x0 += sx
                err += dy
            y0 += sy

    points.append((x1, y1))
    return points


if __name__ == "__main__":
    x0 = 3
    y0 = 2
    x1 = 3
    y1 = 11
    points = get_line(x0, y0, x1, y1)
    print(points)
