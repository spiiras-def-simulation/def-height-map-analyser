import matplotlib.pyplot as plt
import matplotlib

# Utils functions

def visualize(polygons, height, width):
	# Plotting polygons

	# Input:
	#		- polygons
	#		- height of hmap
	#		- width of hmap

	for key in polygons.keys():
		X = []
		Y = []
		for i in range(len(polygons[key])):
			X.append(polygons[key][i][0])
			Y.append(polygons[key][i][1])
		marker = 'ro' if len(X) == 1 else 'r'
		plt.plot(X,Y, marker)
	plt.axis([-width//2 -1, width//2 +1, -height//2 -1, height//2 +1])
	plt.show()

def obstacle_height_detection(hmap, height):
	# Defines points, higher than bound

	# Input:
	#		- heightmap
	#		- maximum height
	# Output:
	#		- array of points

	obstacles = []
	for point in hmap:
		h, w = point
		p = hmap[(h,w)]
		if p.z > height:
			obstacles.append([p.x, p.y])
	return obstacles


def grahamscan(A):
	# Defines boundaries of cluster

	# Input: 
	# 		- array of points [x, y]
	# Output: 
	# 		- indexes of points of boundaries

	n = len(A)
	P = list(range(n))
	if n == 1:
		return [0]
	for i in range(1, n):
		if A[P[i]][0] < A[P[0]][0]:
			P[i], P[0] = P[0], P[i]
	# Insertion-sort
	for i in range(2, n):
		j = i
		while j > 1 and (rotate(A[P[0]], A[P[j-1]], A[P[j]]) < 0): 
			P[j], P[j-1] = P[j-1], P[j]
			j -= 1
	S = [P[0], P[1]]
	for i in range(2, n):
		while rotate(A[S[-2]], A[S[-1]], A[P[i]]) < 0:
			del S[-1]
		S.append(P[i])

	return S

def rotate(A,B,C):
  	return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])