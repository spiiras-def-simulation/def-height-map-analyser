from path_planning.Heightmap import Heightmap

# Height bound to detect obstacles
HEIGHT = 10

def obstacle_height_detection(hmap, height):
	obstacles = []
	for point in hmap:
		h, w = point
		p = hmap[(h,w)]
		if p.z > height:
			obstacles.append(p)
	return obstacles

def main():
	hm = Heightmap()
	hmap, height, width, x_step, y_step, grid_step = hm.prepare_heightmap()
	obstacles = obstacle_height_detection(hmap, HEIGHT)
	print(obstacles)


if __name__ == "__main__":
	main()