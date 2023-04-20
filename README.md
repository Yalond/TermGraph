# Termgraph - Terminal graphing libary

Command line graphing library. Print out graphs using the command line. Prints multiple graphs, handles different colors, and lables. Check out the following exmaple. Adjustable sized graphs. 

![Demo Image](/assets/graphImage.png)

Usage
-----

```python
import numpy as np
import termgraph
from termgraph import tcolors

# Single plot exxample

x = np.linspace(-10, 10, 1000)
y = x.map(lambda x: x * x)

termgraph.plot([x, y])

# Here's an example with multiple plots

x = np.linspace(-10, 10, 1000)
y1 = x.map(lambda x: x ** 2)
y2 = x.map(lambda x: x ** 3)
y3 = x.map(lambda x: x ** 4)

termgraph.plot([x, y1, x, y2, x, y3])

# Here's an example with multiple plots, sleecting the size and color

x = np.linspace(-10, 10, 1000)
y1 = x.map(lambda x: x ** 2)
y2 = x.map(lambda x: x ** 3)
y3 = x.map(lambda x: x ** 4)

termgraph.plot(
    [x, y1, x, y2, x, y3], 
    size=(40, 10),
    colors=[tcolors.RED, tcolors.GREEN, tcolors.BLUE],
    labels=["x^2", "x^3", "x^4"]
)

```




