import Constants as const
from Point import Point
import cv2

# Heightmap class used for generating cell matrix
# heightmap: heightmap vertex list
class Heightmap:
    def __init__(self, map_path, map_distance, map_min_elivation, map_max_elivation):
        self.heightmap = []
        self.map_path = map_path
        self.map_distance = map_distance
        self.map_min_elivation = map_min_elivation
        self.map_max_elivation = map_max_elivation
        self.map_elivation = self.map_max_elivation - self.map_min_elivation
        self.map_i_step = self.map_elivation / 255

# Converting a grayscale image to a heightmap vertex list        
    def heightmap_builder(self):
        print('Map min elivation: ' + str(self.map_min_elivation))
        print('Map max elivation: ' + str(self.map_max_elivation))
        print('Map intensive step: ' + str(self.map_i_step))
        image = cv2.imread(self.map_path, 0)
        self.map_height = image.shape[0]
        self.map_width = image.shape[1]
        self.x_step_size = self.map_distance / (self.map_height - 1)
        self.y_step_size = self.map_distance / (self.map_width - 1)
        print('x_step_size: ' + str(self.x_step_size))
        print('y_step_size: ' + str(self.y_step_size))
        for i in range(image.shape[0]):  # traverses through height of the image
            self.heightmap.append([])
            for j in range(image.shape[1]):  # traverses through width of the image
                x = -self.map_distance / 2 + j * self.x_step_size 
                y = self.map_distance / 2 - i * self.y_step_size
                z = self.map_min_elivation + image[i][j] * self.map_i_step
                p = Point(x, y, z)
                p_id = (str(i), str(j))
                p.set_id(p_id)
                p.set_neighbors_list()
                self.heightmap[i].append(p)


# Converting heightmap vertex dictionary to list
# Input
# dict_hmap: heightmap vertex dictionary

# Output
# h_map: heightmap vertex list
    def convert_to_list(self, dict_hmap):
        h_map = []
        for i in range(self.map_height):
            h_map.append([])
            for j in range (self.map_width):
                key = (str(i), str(j))
                v = dict_hmap[key]
                h_map[i].append(v)
                #print(key)
        return h_map

# Converting heightmap vertex list to dictionary
# Input
# list_hmap: heightmap vertex list

# Output
# h_map: heightmap vertex dictionary
    def convert_to_dict(self, list_hmap):
        h_map = {}
        for i in range(len(list_hmap)):
            for j in range(len(list_hmap[i])):
                key = (str(i), str(j))
                h_map[key] = list_hmap[i][j]
        return h_map             

# Preparing a heightmap for further path planning (generation + converting to dictionary)
    def prepare_heightmap(self):
        self.heightmap_builder()
        hmap = self.convert_to_dict(self.heightmap)
        return hmap, self.map_height, self.map_width, self.x_step_size, self.y_step_size, self.map_min_elivation, self.map_max_elivation

# Finding a Key in a Dictionary by Value
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
