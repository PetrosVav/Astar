import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from IPython.display import HTML

class visualization:
    def __init__(self, S, F):
        '''
          This method initializes an a visualization type object.
          Input: 
          -> S: start point of the search
          -> F: end point
        '''
        self.S = S
        self.F = F
        self.images = []
    
    def draw_step(self, grid, frontier, expanded_nodes):
        '''
          This function is called for designing a frame on the animation (every node expansion)
          Input: 
          -> grid: A map of grid type
          -> frontier: A list of nodes that belong in the same search frotier
          -> expanded_nodes: A list of nodes that have been already expanded
          Returns: None
          This function must be called at least once, because the animation must have at least one frame.
        '''
        image = np.zeros((grid.N, grid.N, 3), dtype=int)
        image[grid.grid == 0] = [255, 255, 255]
        image[grid.grid == 1] = [0, 0, 0]
        
        for node in expanded_nodes:
            image[node] = [0, 0, 128]

        for node in frontier:
            image[node] = [0, 225, 0]

        image[self.S] = [50, 168, 64]
        image[self.F] = [168, 50, 50]
        self.images.append(image)
    
    def add_path(self, path):
        '''
          This path adds the optimal path to the last frame of the animation.
          Input:
          -> path: A list which contains the optimal path (must contain the start and the end node)
          Returns: None
        '''
        for n in path[1:-1]:
            image = np.copy(self.images[-1])
            image[n] = [66, 221, 245]
            self.images.append(image)
        
    def create_gif(self, fps = 30, repeat_delay = 2000):
        if len(self.images) == 0:
            raise EmptyStackOfImages("Error! You have to call 'draw_step' at  first.")
        fig = plt.figure()
        plt.axis('off')
        ims = []
        for img in self.images:
            img = plt.imshow(img)
            ims.append([img])
        ani = animation.ArtistAnimation(fig, ims, interval=1000//fps, blit=True, repeat_delay= repeat_delay)
        plt.close(fig)
        return ani
        
    def save_gif(self, filename, fps = 30):
        '''
            This function recreates and saves the animation to a file.
            Input:
            -> The name of the file followed by the suffix .gif
            Returns: (None)
        '''
        ani = self.create_gif(fps)
        writer = PillowWriter(fps= fps)
        ani.save(filename, writer=writer)

    def show_gif(self, fps= 30, repeat_delay = 2000):
        '''
            This function shows, inline, the animation.
            Input:
            -> fps: frames per second
            Returns: The animation object
            Exceptions: EmptyStackOfImages if the animation does not have a single frame, meaning that draw_step has never been called.
        '''
        ani = self.create_gif(fps, repeat_delay)
        # return HTML(ani.to_html5_video())
        return HTML(ani.to_jshtml())

    def show_last_frame(self):
        '''
            This function shows, inline, the last frame.
            Input: None
            Returns: The object that show the image.
            Exceptions: EmptyStackOfImages if the animation does not have a single frame, meaning that draw_step has never been called.
        '''
        if len(self.images) == 0:
            raise EmptyStackOfImages("Error! You have to call 'draw_step' at  first.")
        else:
            plt.imshow(self.images[-1])


class EmptyStackOfImages(Exception):
    pass
