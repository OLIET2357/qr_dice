# https://qiita.com/Inoue_Minoru/items/7291b83ab659ca629bca#%E7%AB%8B%E6%96%B9%E4%BD%93%E6%AD%A3%E5%85%AD%E9%9D%A2%E4%BD%93%E4%BD%9C%E3%82%8A%E3%81%9F%E3%81%84

import numpy as np
from stl import mesh


def cube_model(scaleX=1, scaleY=1, scaleZ=1):
    scaleX = scaleX / 2
    scaleY = scaleY / 2
    scaleZ = scaleZ / 2

    vertices = np.array([
        [-1*scaleX, -1*scaleY, -1*scaleZ],
        [+1*scaleX, -1*scaleY, -1*scaleZ],
        [+1*scaleX, +1*scaleY, -1*scaleZ],
        [-1*scaleX, +1*scaleY, -1*scaleZ],
        [-1*scaleX, -1*scaleY, +1*scaleZ],
        [+1*scaleX, -1*scaleY, +1*scaleZ],
        [+1*scaleX, +1*scaleY, +1*scaleZ],
        [-1*scaleX, +1*scaleY, +1*scaleZ]])

    faces = np.array([
        [0, 3, 1],
        [1, 3, 2],
        [0, 4, 7],
        [0, 7, 3],
        [4, 5, 6],
        [4, 6, 7],
        [5, 1, 2],
        [5, 2, 6],
        [2, 3, 6],
        [3, 7, 6],
        [0, 1, 5],
        [0, 5, 4]])

    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    cube.remove_duplicate_polygons = True
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]

    return cube
