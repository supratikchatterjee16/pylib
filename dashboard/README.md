# Dashboard

A socket wrapper over a Dash and Plotly utility.
The following command gives the subsequent required steps :

```python3
from dashboard.dashboard_client import DashboardClient
plotter = DashClient()
```
Some sample commands that can be executed are : 

```python3
plotter.silent = False

plotter.clear()

plotter.update(title = "Hello World")
plotter.make_subplot(rows = 2, cols = 2, height = 700)
plotter.add_trace(x = x1, y = y1.tolist(), type = "scatter", name = "hello world", row = 1, col = 1)
plotter.add_trace(x = x1, y = y1.tolist(), type = "scatter", name = "sin", row = 1, col = 1)
plotter.add_trace(x = x2, y = y2, type = "scatter", name = "smooth-step", row = 1, col = 2, opacity=0.25)
plotter.add_trace(x = x2, y = y3.tolist(), type = "bar", name = "random something else", row = 2, col = 1, opacity=0.5)

```

The code above produces the following image : 

![Screen Shot of dashboard in action](dashboard_screenshot.png)