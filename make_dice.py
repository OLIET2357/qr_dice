import random
import qrcode
import numpy as np
from cube_model import cube_model
from stl import mesh


def cube_at(x, y, z):
    cube = cube_model(1, 1, 1)
    cube.translate(np.array([x, y, z]))
    return cube


def voxel_to_mesh(voxel):
    assert len(voxel.shape) == 3
    meshes = []
    for i in range(voxel.shape[0]):
        for j in range(voxel.shape[1]):
            for k in range(voxel.shape[2]):
                if voxel[i][j][k]:
                    meshes.append(cube_at(i, j, k).data)
    return mesh.Mesh(np.concatenate(meshes))


def reversible_qr(data1, data2):
    qr1 = qrcode.QRCode(
        version=7, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr1.add_data(data1)
    qr1.make(fit=True)

    qr2 = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr2.add_data(data2)
    qr2.make(fit=True)

    m1 = qr1.modules
    m2_r = np.rot90(np.fliplr(qr2.modules))

    for i in range(m2_r.shape[0]):
        for j in range(m2_r.shape[1]):
            m1[i][j] = m2_r[i][j]

    for i in range(21):
        m1[i][21] = False
        m1[i][22] = False

    for j in range(21):
        m1[21][j] = False
        m1[22][j] = False

    return m1


m1_6 = reversible_qr('1', '6')
m2_5 = reversible_qr('2', '5')
m3_4 = reversible_qr('3', '4')

assert len(m1_6) == len(m2_5) == len(m3_4)

S = len(m1_6)

voxel_qr = np.zeros((S,)*3)


for i in range(S):
    for j in range(S):
        for k in range(S):
            voxel_qr[i][j][k] = m1_6[i][j] and \
                m2_5[j][k] and m3_4[k][i]

c1_6 = np.zeros((S, S))
c2_5 = np.zeros((S, S))
c3_4 = np.zeros((S, S))
for i in range(S):
    for j in range(S):
        for k in range(S):
            if voxel_qr[i][j][k]:
                c1_6[i][j] += 1
                c2_5[j][k] += 1
                c3_4[k][i] += 1

for i in random.sample(range(S), S):
    for j in random.sample(range(S), S):
        for k in random.sample(range(S), S):
            if c1_6[i][j] > 1 and c2_5[j][k] > 1 and c3_4[k][i] > 1:
                voxel_qr[i][j][k] = False
                c1_6[i][j] -= 1
                c2_5[j][k] -= 1
                c3_4[k][i] -= 1

mesh_qr = voxel_to_mesh(voxel_qr)

mesh_qr.save('qr_dice.stl')
