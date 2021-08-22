import sys
import json
import numpy as np
from sklearn.cluster import DBSCAN
import requests

from Heightmap import Heightmap
import utils

# Map params
MAP_PATH = sys.argv[1]
MAP_DISTANCE = float(sys.argv[2])
MAP_MIN_ELIVATION = float(sys.argv[3])
MAP_MAX_ELIVATION = float(sys.argv[4])
UAV_MAX_ELIVATION = float(sys.argv[5])

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
		rects[int(key)] = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
	return rects

def main():
	# Data preparation
	hm = Heightmap(MAP_PATH, MAP_DISTANCE, MAP_MIN_ELIVATION, MAP_MAX_ELIVATION)
	hmap, height, width, x_step, y_step, map_min_elivation, map_max_elivation = hm.prepare_heightmap()
	obstacles = utils.obstacle_height_detection(hmap, UAV_MAX_ELIVATION)

	# Clustering
	clusters = dict()
	if UAV_MAX_ELIVATION < map_max_elivation:
			clustering = DBSCAN(eps=3, min_samples=1).fit(np.array(obstacles))
			for i in clustering.labels_:
				clusters[i] = []
			for i in range(len(clustering.labels_)):
				clusters[clustering.labels_[i]] += [obstacles[i]]

	# Define and visualize rectangles
	rects = define_rectangles(clusters)

	# Request send produced rectangles
	result = requests.post('http://localhost:5252/areas', data = { 'areas': json.dumps(rects) })
	if result.status_code == 200:
		print('Add areas to system')
	else:
		print('Problem with adding areas to sustem with code', result.status_code)

if __name__ == "__main__":
	main()