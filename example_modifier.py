import numpy as np
import pandas as pd

from modifier import action, Modifier


@action(tags=["logical"])
def fix_width_lt_height(width, height):
    '''Make sure that width is greater than height.'''
    return {"width": np.maximum(width, height),
            "height": np.minimum(width, height)}


modifier = Modifier()
modifier.add_rule(fix_width_lt_height)

# alternatively
modifier.add_rule(rule="width = width + height",
                  condition="width>height",
                  name="check_dimensions",
                  description="Check that width is greater than height",
                  tags=["logical"])

# Or load from yaml file
# modifier = Modifier.from_file("modifier.yaml")

df = pd.DataFrame([
    {"width": 1, "height": 2},
    {"width": 2, "height": 1},
    {"width": 1, "height": 1},
    {"width": 2, "height": 2},
])

res = modifier.run(df)
print(res)
