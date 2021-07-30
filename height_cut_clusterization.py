import matplotlib.pyplot as plt
import numpy as np
from path_planning.Heightmap import Heightmap
from sklearn.cluster import DBSCAN
import utils

# Height bound to detect obstacles
HEIGHT = 10

def define_rectangles(clusters):
	# Defines rectangles, that fit points in clusters

	# Input:
	#		- clusters {key: points}
	# Output:
	#		- rectangles [(xmin, ymin), width, height]

	rects = {}
	for key in clusters.keys():
		points = clusters[key]
		xmin, ymin, xmax, ymax = utils.rect_corners(points)
		width_rect = xmax - xmin
		height_rect = ymax - ymin
		rects[key] = [(xmin, ymin), width_rect, height_rect]
	return rects

def define_polygons(clusters):
	# Defines polygons, that fit points in clusters

	# Input:
	#		- clusters {key: points}
	# Output:
	#		- polygons {key: points}

	bounds = {}
	for key in clusters.keys():
		points = clusters[key]
		boundaries_indexes = utils.grahamscan(points)
		bounds[key] = boundaries_indexes
	polygons = {}
	for key in clusters.keys():
		polygons[key] = []
		for i in bounds[key]:
			polygons[key].append(clusters[key][i])
	return polygons

def main():
	# Data preparation
	hm = Heightmap()
	hmap, height, width, x_step, y_step, grid_step = hm.prepare_heightmap()
	obstacles = utils.obstacle_height_detection(hmap, HEIGHT)

	# Clustering
	clustering = DBSCAN(eps=3, min_samples=1).fit(np.array(obstacles))
	clusters = dict()
	for i in clustering.labels_:
		clusters[i] = []
	for i in range(len(clustering.labels_)):
		clusters[clustering.labels_[i]] += [obstacles[i]]

	# Define and visualize rectangles
	rects = define_rectangles(clusters)
	utils.visualize_rectangles(clusters, rects, width, height)

	# # Define and visualize polygons
	# polygons = define_polygons(clusters)
	# utils.visualize_polygons(polygons, width, height)

if __name__ == "__main__":
	main()