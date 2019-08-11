# CSV Utility

Made to load csv files mainly.
Make use of pandas library for better things.

```python3
import pandas as pd
csv_file_as_dict = pd.read_csv("actors.csv").to_dict(orient="row")
```
