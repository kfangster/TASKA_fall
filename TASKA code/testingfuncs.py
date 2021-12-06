import Quaternion
from Quaternion import _AXES2TUPLE, relative, to_euler

calibrator =[-0.7151, 0.016, 0.0146, 0.6986]
tracker = [-0.1321, -0.6958, -0.6965, 0.1149]


quat_combine = relative(calibrator,tracker)
print(quat_combine)

euler_angs = to_euler(quat_combine, axes='sxyz')
print(euler_angs)

print(type(calibrator[1]))