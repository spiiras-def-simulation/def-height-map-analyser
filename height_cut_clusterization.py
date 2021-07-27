import matplotlib.pyplot as plt
import numpy as np
from path_planning.Heightmap import Heightmap
from sklearn.cluster import DBSCAN
from utils import obstacle_height_detection, grahamscan

# Height bound to detect obstacles
HEIGHT = 6


def main():
	# Data preparation
	hm = Heightmap()
	hmap, height, width, x_step, y_step, grid_step = hm.prepare_heightmap()
	obstacles = obstacle_height_detection(hmap, HEIGHT)

	# Clustering
	clustering = DBSCAN(eps=3, min_samples=1).fit(np.array(obstacles))
	clusters = dict()
	for i in clustering.labels_:
		clusters[i] = []
	for i in range(len(clustering.labels_)):
		clusters[clustering.labels_[i]] += [obstacles[i]]

	# Define polygons
	bounds = {}
	for key in clusters.keys():
		points = clusters[key]
		boundaries_indexes = grahamscan(points)
		bounds[key] = boundaries_indexes

	polygons = {}
	for key in clusters.keys():
		X = []
		Y = []
		polygons[key] = []
		for i in bounds[key]:
			polygons[key].append(clusters[key][i])
			X.append(clusters[key][i][0])
			Y.append(clusters[key][i][1])

		# For visialuzation
		#plt.plot(X,Y, 'r')

	# For visualization
	#plt.axis([-width//2, width//2, -height//2, height//2])
	#plt.show()

if __name__ == "__main__":
	main()