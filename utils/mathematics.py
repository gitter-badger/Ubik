def percentile(x, ys):
    sz_y = len(ys)
    if sz_y == 0:
        return -1
    elif sz_y == 1:
        return 0.
    else:
        return sum(y < x for y in ys)/ float(len(ys) - 1) * 100
