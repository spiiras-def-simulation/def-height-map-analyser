import matplotlib.pyplot as plt
import numpy as np
from path_planning.Heightmap import Heightmap
from sklearn.cluster import DBSCAN
from utils import obstacle_height_detection, grahamscan, visualize

# Height bound to detect obstacles
HEIGHT = 10


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
		polygons[key] = []
		for i in bounds[key]:
			polygons[key].append(clusters[key][i])

	# Visuzlization
	visualize(polygons, height, width)

if __name__ == "__main__":
	main()