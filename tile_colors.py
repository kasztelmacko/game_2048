import seaborn as sns
from matplotlib.colors import to_hex

n_colors = 17
color_palette = sns.color_palette("OrRd", n_colors)
hex_palette = [to_hex(color, keep_alpha=False) for color in color_palette]
tile_colors = {str(2**i): hex_palette[i] for i in range(n_colors)}


