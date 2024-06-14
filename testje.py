import pandas as pd
from pymodify import Validator, check

@check
def check_proportions(width, height):
    return 2 * width < height


data = pd.DataFrame([
    {"width": 3, "height": 7,},
    {"width": 3, "height": 5,}
])


validator = Validator()
validator.add(check_proportions)
validator.add("2 * width > height", name="check_proportions2")
validator.load_py("example_checks.py")
result = validator.run(data)
print(result)
