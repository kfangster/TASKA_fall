import numpy as np
angles = [0.1,0.2,0.3,0.4,0.5,0.6]
angles1 = np.dot(80,angles)
angles = angles1
print(angles)
angles = [min(max(20, angle), 80) for angle in angles ]
print(angles)
angles = [(angles[0]-20)/60,(angles[1]-20)/60,(angles[2]-20)/60,(angles[3]-20)/60,(angles[4]-20)/60,(angles[5]-20)/60]

print(angles[5])