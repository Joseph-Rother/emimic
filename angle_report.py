import numpy as np

def get_angles(point_1,point_2,point_3):

    a = np.array(point_1)
    b = np.array(point_2)
    c = np.array(point_3)
    ba = a - b
    bc = c - b
    cosa = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosa)

    return (np.degrees(angle))
