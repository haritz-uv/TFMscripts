import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from scipy.ndimage import rotate
"Functions used in the image treatment."

def square_corners_coordinates(eclick, erelease):
    """Calculate the coordinates of the corners of a square region selected by the user."""

    x_start, y_start = int(eclick.xdata), int(eclick.ydata)
    x_end, y_end = int(erelease.xdata), int(erelease.ydata)

    # Ensure the coordinates are in the correct order:
    x_start, x_end = sorted([x_start, x_end])
    y_start, y_end = sorted([y_start, y_end])
    print(f"Selected square region: ({x_start}, {y_start}) to ({x_end}, {y_end})")
    return x_start, y_start, x_end, y_end

def quick_plot_img(img_path):
    """plot an image and allow the user to select a square region. Shows the coordinates of the selected region in the console."""
    img = plt.imread(img_path)
    fig, ax = plt.subplots(figsize = (8, 8))
    ax.imshow(img, cmap='gray', origin='lower')
    ax.set_title("Click and drag to select a square region")
    ax.axis('on')

    # Create a RectangleSelector
    rect_selector = RectangleSelector(ax, onselect=square_corners_coordinates, useblit=True,
                                       button=[1],  # Left mouse button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)

   


    plt.show()

img_path = r"G:\Mi unidad\Experiments\Materials\Multiferroic\hm_zarcillo\afm\00921\Image00921.png"


quick_plot_img(img_path)