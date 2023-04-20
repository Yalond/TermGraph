from typing import Union
import math
from .tcolors import tcolors


def _hex_to_dots(a, b):
    return chr(10240 + b * 16 + a)

def _panel_to_dots(panel):
    # This is the order that the unicode consortium decided
    # to arrange braille in. It is what it is.
    steps = [0, 3, 1, 4, 2, 5, 6, 7]

    v = sum([(2 ** a) * b for a, b in zip(steps, panel)])
    a = v % 16
    b = int(v/16)
    return _hex_to_dots(a, b)

def _inverse_lerp(a, b, t):
    return (b - t)/(b - a)

def _lerp(a, b, t):
    return a + (b - a) * t

def _normalize_list(xs, min_v = None, max_v = None):
    min_x = min_v if min_v != None else min(xs)
    max_x = max_v if max_v != None else max(xs)
    return (_inverse_lerp(min_x, max_x, x) for x in xs)

def _checker(pairs):
    return lambda x, y: 1 if (x, y) in pairs else 0

def _plot_points(
        xs: list[float], 
        ys: list[float], 
        width:int, 
        height:int, 
        color:str=tcolors.BLUE
        ) -> list[list[str]]:

    out = []
    white_space = "⠀"
    norm_xs = [int(x * (width - 0)) - 0 for x in xs]
    norm_ys = [int(y * (height - 4)) for y in ys]
    check = _checker(set(zip(norm_xs, norm_ys)))
    window_width = 2
    window_height = 4
    for y in range(0, height - window_height, window_height):
        out_row = []
        for x in range(0, width - window_width, window_width):
            window = [check(x, y), check(x + 1, y),
                      check(x, y + 1), check(x + 1, y + 1),
                      check(x, y + 2), check(x + 1, y + 2),
                      check(x, y + 3), check(x + 1, y + 3),
                      ]

            char = _panel_to_dots(window)
            if char != white_space:
                char = color + char + tcolors.ENDC
            out_row.append(char)

        out.append(out_row)
    return out


def create_box(width, height, color = tcolors.YELLOW):

    bl = "╰"
    br = "╯"
    tl = "╭"
    tr = "╮"
    sv = "│"
    sh = "─"

    mw = width - 1
    mh = height -1
    out = []

    for y in range(height):
        current_row = []
        for x in range(width):

            st = color
            if x == 0 and y == 0: st += tl
            elif x == mw and y == mh: st += br
            elif x == 0 and y == mh: st += bl
            elif x == mw and y == 0: st += tr
            elif x == 0 or x == mw: st += sv
            elif y == 0 or y == mh: st += sh
            else: st += " "
            st += tcolors.ENDC
            current_row.append(st)

        out.append(current_row)
        current_row = ""
    return out

def _pad_layer(layer):
    out = []
    height = len(layer)
    width = len(layer[0])
    out.append([" " for _ in range(width + 2)])
    for row in layer:
        out.append([" "] + row[:] + [" "])
    out.append([" " for _ in range(width + 2)])
    return out

def _combine_layers(layer_stack):
    white_space = set([" ", "⠀"])
    out = layer_stack[0][:]
    for layer in layer_stack[1:]:
        for line_index, line in enumerate(layer):
            for char_index, char in enumerate(line):
                if not (char in white_space):
                    out[line_index][char_index] = char
    return out

def _print_layer(layer):
    print("\n".join(["".join(line) for line in layer]))

def _print_size(xs, name):
    print(f"{name} x: {len(xs[0])} y: {len(xs)}")

def _plot_vals(x, y):
    for i, _ in enumerate(x):
        print(f"{x[i]}, {y[i]})")

def _axis(height, min_v, max_v):
    out = []
    for i in range(height):
        t = _lerp(min_v, max_v, _inverse_lerp(0, height, i))
        out.append("{:.3f}".format(t))
    max_len = len(max(out, key=lambda x: len(x)))
    return [[" " * (max_len - len(x)) + x + " - "] for x in out]
        
def _append_layers_h(a, b):
    return [a + b for a, b in zip(a, b)]

_default_term_colors = [tcolors.BLUE, tcolors.GREEN, tcolors.RED, tcolors.YELLOW, tcolors.CYAN]

def _plot_lables(width, height, labels, color_list):
    label_list = []
    if (labels != None):
        current_row = []
        for index, label in enumerate(labels):
            current_label = tcolors.c(color_list[index%len(color_list)], label)
            currnet_label = list(label)
            if (len(current_row) + len(current_label) > width):
                label_list.append(current_row)
                current_row = []
            current_color = color_list[index%len(color_list)]
            new_item = [f"{current_color}{x}{tcolors.ENDC}" for x in list(label)] 
            current_row.extend(new_item + [" "])

        if (len(current_row) > 0): label_list.append(current_row)

    box = create_box(width + 2, len(label_list) + 2)
    label_list = _pad_layer(label_list)
    label_list_box = _combine_layers([box, label_list])
    _print_layer(label_list_box)
 

def plot(plots: list[list[float]], 
         size: tuple[float, float] = (80, 15),
         colors:Union[list[str], None] = None, 
         labels: Union[list[str], None] = None):

    """Plotting function, pass data to this function to plot it to the terminal.

    Parameters:
        plots (List<List<float>): A list of values to plot. [x1, y1, x2, y2, x3, y3].
        width (int): The width of the plot.
        height (int): the height of the plot.
        colors (List<string>): A list of termcolors, to be applied to the graphs.
        labels (List<string>): A list of labels for the plots.

    """
    width, height = size

    color_list = colors if colors != None else _default_term_colors

    layers = [create_box(width + 2, height + 2)]

    max_x = float("-inf")
    min_x = float("inf")
    max_y = float("-inf")
    min_y = float("inf")

    for i in range(0, len(plots), 2):
        max_x = max(max_x, max(plots[i]))
        min_x = min(min_x, min(plots[i]))
        max_y = max(max_y, max(plots[i + 1]))
        min_y = min(min_y, min(plots[i + 1]))
    
    norm_plots = []
    for i in range(0, len(plots), 2):
        norm_plots.append(list(_normalize_list(plots[i], min_x, max_x)))
        norm_plots.append(list(_normalize_list(plots[i + 1], min_y, max_y)))

    for i in range(0, len(norm_plots), 2):
        color = color_list[int(i/2)%len(color_list)]
        layers.append(_pad_layer(_plot_points(norm_plots[i], norm_plots[i + 1], width * 2 + 1, height * 4 + 2, color)))

    res = _combine_layers(layers)
    _print_layer(res)
    if labels != None:
        _plot_lables(width, height, labels, color_list)

def main():

    count = 3000
    min_val = -10
    max_val = 10
    x = [_lerp(min_val, max_val, t/count) for t in range(count)]
    y1 = [math.sin(v * 0.2) *  1 for v in x]
    y2 = [math.sin(v * 0.4) *  0.8  for v in x]
    y3 = [math.sin(v * 0.7) *  0.7  for v in x]
    y4 = [math.sin(v * 1) *  0.6  for v in x]
    y5 = [math.sin(v * 1.2) *  0.5  for v in x]
    plot([x, y1, x, y2, x, y3, x, y4, x, y5], (130, 20), 
         labels=["sin(x * 0.2) * 1", "sin(x * 0.4) * 0.8", "sin(x * 0.7) * 0.7", "sin(x * 1) * 0.6", "sin(x * 1.2) * 0.5"])

if __name__ == "__main__":
    main()