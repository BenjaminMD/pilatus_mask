import numpy as np
import matplotlib.pyplot as plt
import toml

class PilatusMask:
    def __init__(self):
        self.x_size, self.y_size = 1679, 1475
        self.pixel_size = 1.72e-4
        self.e = 1
        self.x_len = self.x_size * self.pixel_size
        self.y_len = self.y_size * self.pixel_size
        self.regions = np.array([[488, 494, None, None],
                                 [982, 988, None, None],
                                 [None, None, 196, 212],
                                 [None, None, 408, 424],
                                 [None, None, 620, 636],
                                 [None, None, 832, 848],
                                 [None, None, 1044, 1060],
                                 [None, None, 1256, 1272],
                                 [None, None, 1468, 1484]])
        self.x_submodules = np.concatenate([
                np.arange(61, 428, 61),
                np.arange(555, 922, 61),
                np.arange(1049, 1416, 61),
                ])
        y_region = self.regions[:,3]
        y_region = y_region[y_region != None]
        self.y_submodules = np.concatenate([y_region + 98, [98]])
        self.mask = np.zeros((self.x_size, self.y_size))
        for y1, y2, x1, x2 in self.regions:
            if y1 is None and y2 is None:
                self.mask[x1-1-self.e:x2+self.e,:] = +1
            else:
                self.mask[:,y1-1-self.e:y2+self.e] = +1
    
    def save_mask(self, filename):
        np.save(filename, self.mask)
    
    def plot_mask(self):
        fig, ax = plt.subplots()
        ax.imshow(self.mask, cmap='binary', origin='lower', extent=[0, self.x_size, 0, self.y_size], aspect='equal')
        ax.set(xlabel='$x$ Pixel / -', ylabel='$y$ Pixel / -')

        if self.p1:
            ax.axvline(self.p1/self.x_len * self.x_size, color='r', linestyle='--')
            ax.axhline(self.p2/self.y_len * self.y_size, color='r', linestyle='--')

            # plot from p1 p2 to corner
            print(self.corner)
            ax.plot([self.p1/self.x_len * self.x_size, self.corner[0]], [self.p2/self.y_len * self.y_size, self.corner[1]], color='r', linestyle='--')
        plt.show()
    
    def sub_grid_masking(self):
        for x in self.x_submodules:
            self.mask[:,x-2:x+1] = +1
        for y in self.y_submodules:
            self.mask[y-2:y+1,:] = +1

    def combine_mask(self, path_to_mask):
        mask = np.load(path_to_mask)
        self.mask = np.logical_or(self.mask, mask).astype(int)

    def read_poni(self, path_to_poni):
        with open(path_to_poni, 'r') as f:
            p1, p2 = f.readlines()[6:8]
        self.p1 = float(*p1.split()[1:])
        self.p2 = float(*p2.split()[1:])
        self.identify_furthest_corner()
        

        print(p1, p2)

    def identify_furthest_corner(self):
        c1 = np.array([self.x_size, self.y_size])
        c2 = np.array([0, 0])
        c3 = np.array([self.x_size, 0])
        c4 = np.array([0, self.y_size])

        corners = np.array([c1, c2, c3, c4])
        self.pixel_p1 = self.p1 / self.x_len * self.x_size
        self.pixel_p2 = self.p2 / self.y_len * self.y_size
        distances = np.linalg.norm(corners - np.array([self.pixel_p1, self.pixel_p2]), axis=1)
        self.corner = corners[np.argmax(distances)]


def main():
    mask = PilatusMask()
    mask.sub_grid_masking()
    mask.combine_mask('/home/ben/DESY_PDF/0_data/maskMZ.npy')
    # mask.combine_mask('/home/ben/DESY_PDF/0_data/config/mask.npy')
    mask.plot_mask()
    mask.save_mask('combined_subsub_grid_mask.npy')

        
if __name__ == '__main__':
    main()
