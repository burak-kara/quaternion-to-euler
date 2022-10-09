import glob
import os
import math as m
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R

ROOT_FOLDER = "results\\uid-*"
INNER_FOLDER = "\\test0\\"
HEADS = "heads"
VIDEOS = ["Diving-2OzlksZBTiA\\*", "Paris-sJxiPiAaB4k\\*", "Rhino-training-7IWp875pCxQ\\*",
		  "Rollercoaster-8lsB-P8nGSM\\*", "Timelapse-CIw8R8thnm8\\*", "Venise-s-AJRFQuAtE\\*"]

folders = glob.glob(ROOT_FOLDER)

try:
	os.makedirs(HEADS)
except:
	print("heads folder is exist. Dont forget to create a backup")


# sys.exit(0)

def conj(q):
	w, x, y, z = q
	return w, -x, -y, -z


def norm(q):
	w, x, y, z = q
	return round(m.sqrt(m.pow(w, 2) + m.pow(x, 2) + m.pow(y, 2) + m.pow(z, 2)), 2)


def qv(q1, v1):
	q2 = (0,) + v1
	# return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]
	return mult(mult(q1, q2), conj(q1))


def calc_atan2(q):
	w, x, y, z = q
	return 2 * m.atan2(m.sqrt(m.pow(x, 2) + m.pow(y, 2) + m.pow(z, 2)), w)


def find_axis_angle(q):
	w, x, y, z = q
	theta = m.degrees(2 * m.acos(w))
	X = x / (m.sqrt(1 - w * w))
	Y = y / (m.sqrt(1 - w * w))
	Z = z / (m.sqrt(1 - w * w))
	return theta, X, Y, Z


def axis_to_euler(axis_angle):
	angle, x, y, z = axis_angle
	yaw = m.atan2(y * m.sin(angle) - x * z * (1 - m.cos(angle)), 1 - (y * y + z * z) * (1 - m.cos(angle)))
	pitch = m.asin(x * y * (1 - m.cos(angle)) + z * m.sin(angle))
	roll = m.atan2(x * m.sin(angle) - y * z * (1 - m.cos(angle)), 1 - (x * x + z * z) * (1 - m.cos(angle)))
	return yaw, pitch, roll


# def vv(q, n):
# 	n = (0,) + n
# 	return mult(mult(q, n), conj(q))


def mult(q1, q2):
	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2
	w = round(w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, 3)
	x = round(w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, 3)
	y = round(w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2, 3)
	z = round(w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2, 3)
	return w, x, y, z


def quaternion_to_euler(w, x, y, z):
	t0 = 2 * (w * x + y * z)
	t1 = 1 - 2 * (x * x + y * y)
	X = m.atan2(t0, t1)

	t2 = 2 * (w * y - z * x)
	t2 = 1 if t2 > 1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = m.asin(t2)

	t3 = 2 * (w * z + x * y)
	t4 = 1 - 2 * (y * y + z * z)
	Z = m.atan2(t3, t4)

	# return X * 180 / m.pi, Y * 90 / m.pi, Z * 180 / m.pi
	# return X, Y, Z
	return m.degrees(X), m.degrees(Y), m.degrees(Z)


def quaternion_to_euler_wu(qx, qy, qz, qw):
	X = 2 * (qx * qz + qy * qw)
	Y = 2 * (qy * qz - qx * qw)
	Z = 1 - 2 * (qx * qx + qy * qy)

	# return X * 180 / m.pi, Y * 90 / m.pi, Z * 180 / m.pi
	return X, Y, Z


def quaternion_to_euler2(a, b, c, d):
	# https://www.allaboutcircuits.com/technical-articles/dont-get-lost-in-deep-space-understanding-quaternions/
	mat = []
	row_1 = []
	row_1.append(a * a + b * b - c * c - d * d)
	row_1.append(2 * (b * c - a * d))
	row_1.append(2 * (b * d + a * c))

	row_2 = []
	row_2.append(2 * (b * c + a * d))
	row_2.append(a * a - b * b + c * c - d * d)
	row_2.append(2 * (c * d - a * b))

	row_3 = []
	row_3.append(2 * (b * d - a * c))
	row_3.append(2 * (c * d + a * b))
	row_3.append(a * a - b * b - c * c + d * d)

	mat.append(row_1)
	mat.append(row_2)
	mat.append(row_3)
	# return X * 180 / m.pi, Y * 90 / m.pi, Z * 180 / m.pi
	return mat


def get_quaternion_from_euler(roll, pitch, yaw):
	"""
	Convert an Euler angle to a quaternion.

	Input
	  :param roll: The roll (rotation around x-axis) angle in radians.
	  :param pitch: The pitch (rotation around y-axis) angle in radians.
	  :param yaw: The yaw (rotation around z-axis) angle in radians.

	Output
	  :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
	"""
	qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
	qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
	qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
	qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

	return [qx, qy, qz, qw]


# print(quaternion_to_euler_wu(0.5, 0.5, 0.5, 0.5))
# print(quaternion_to_euler2(0.5, 0.5, 0.5, 0.5))
# print(quaternion_to_euler(0.5, 0.5, 0.5, 0.5))
# print(qv_mult(q1, i))

# qq = get_quaternion_from_euler(0, 0, m.radians(-162.5))
qq = get_quaternion_from_euler(m.radians(-162.5), 0, 0)
print(qq)
print(R.from_quat(qq).as_euler("XYZ", degrees=True))

r = R.from_euler('YXZ', [-12.5, 0, 0], degrees=True)
print(r.as_euler("YXZ", degrees=True))

print("----------------")
qq = [0.5, 0.5, 0.5, 0.5]
print(R.from_quat(qq).as_euler("XYZ", degrees=True))
print(R.from_quat(qq).as_euler("XZY", degrees=True))
print(R.from_quat(qq).as_euler("YXZ", degrees=True))
print(R.from_quat(qq).as_euler("YZX", degrees=True))
print(R.from_quat(qq).as_euler("ZXY", degrees=True))
print(R.from_quat(qq).as_euler("ZYX", degrees=True))
print(R.from_quat(qq).as_rotvec(degrees=True))
print(R.from_quat(qq).as_matrix())
print(quaternion_to_euler2(0.5, 0.5, 0.5, 0.5))

sys.exit(1)

print("----------------")
q1 = -0.015, 0.948, -0.063, -0.31
q2 = -0.31, -0.015, 0.948, -0.063
i = (1.0, 0.0, 0.0)
j = (0.0, 1.0, 0.0)
k = (0.0, 0.0, 1.0)

print(q1)
print(conj(q1))
print("----------------")
print(qv(q1, i))
print(qv(q2, i))
print("----------------")
print(qv(q1, j))
print(qv(q2, j))
print("----")
print(qv(q1, k))
print(qv(q2, k))
print("*****************************")
q1_conv = quaternion_to_euler_wu(-0.015, 0.948, -0.063, -0.31)
q2_conv = quaternion_to_euler_wu(-0.31, -0.015, 0.948, -0.063)
print(q1_conv)
print(q2_conv)
# q1_conv_atan = calc_atan2(q1_conv)
# q2_conv_atan = calc_atan2(q2_conv)
# print(q1_conv_atan)
# print(q2_conv_atan)
print("/////////////////////////////////")
norm1 = norm(q1)
norm2 = norm(q2)
print("----")
q1_i = qv(q1, i)
q2_i = qv(q2, i)
q1_j = qv(q1, j)
q2_j = qv(q2, j)
q1_k = qv(q1, k)
q2_k = qv(q2, k)

print(q1_i)
print(q2_i)
print(q1_j)
print(q2_j)
print(q1_k)
print(q2_k)

q1_i_atan = calc_atan2(q1_i)
print(q1_i_atan)
print(m.degrees(q1_i_atan))
q2_i_atan = calc_atan2(q2_i)
print(q2_i_atan)
print(m.degrees(q2_i_atan))
q1_j_atan = calc_atan2(q1_j)
print(q1_j_atan)
print(m.degrees(q1_j_atan))
q2_j_atan = calc_atan2(q2_j)
print(q2_j_atan)
print(m.degrees(q2_j_atan))
q1_k_atan = calc_atan2(q1_k)
print(q1_k_atan)
print(m.degrees(q1_k_atan))
q2_k_atan = calc_atan2(q2_k)
print(q2_k_atan)
print(m.degrees(q2_k_atan))

print("----")

# q1_norm_i = norm(q1_i)
# q2_norm_i = norm(q2_i)
# q1_norm_j = norm(q1_j)
# q2_norm_j = norm(q2_j)
# q1_norm_k = norm(q1_k)
# q2_norm_k = norm(q2_k)

print("----")
axis1 = find_axis_angle(q1)
euler1 = axis_to_euler(axis1)
print(axis1)
print(euler1)
axis2 = find_axis_angle(q2)
euler2 = axis_to_euler(axis2)
print(axis2)
print(euler2)

sys.exit(1)
# for each user folder
for i in range(len(folders)):
	folder = folders[i]
	uid = folder.split('\\')[-1][4:]

	# for each video folder inside a user folder
	for v_i in range(len(VIDEOS)):
		video = VIDEOS[v_i]  # Set video
		video_name = video.split('-')[0]
		path = folder + INNER_FOLDER + video
		log_file = glob.glob(path)
		if log_file:
			with open(log_file[0]) as file:
				with open(HEADS + "\\head_" + video_name.lower() + "_" + str(i), "w") as extracted:
					lines = file.readlines()
					for line in lines:
						line = line.replace('\n', '').split()
						line[0] = int(float(line[0]) * 1000)  # convert timestamp from seconds to milliseconds
						del line[1]  # clear frame id
						# line[1:] = quaternion_to_euler2(float(line[1]), float(line[2]), float(line[3]), float(line[4]))
						# print(quaternion_to_euler(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
						# print(quaternion_to_euler2(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
						print(quaternion_to_euler(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
					# extracted.write(modified_line)
					sys.exit(1)
