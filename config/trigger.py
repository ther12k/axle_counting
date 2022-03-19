'''
    Trigger camera to take a picture. and process it.
    --------A1--------A2--------B1--------B2----------
    |       |         |         |          |         |
    |       |         |         |          |         |
    |       |         |         |          |         |
    |       |         |         |          |         |
    --------A1--------A2--------B1--------B2----------
    if deam signal is detected, value of A1, A2, B1, B2 will be 1.
    Trigger format:
    [A1, A2, B1, B2]
'''
trigger_camera = []