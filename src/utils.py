def clamp(x: float, min_clamp: float, max_clamp: float):
    if x < min_clamp:
        return min_clamp
    if x > max_clamp:
        return max_clamp
    return x
