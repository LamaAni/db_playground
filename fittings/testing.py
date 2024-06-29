# %% Tester
import os
import pandas
from matplotlib import pyplot as plt
from utils.constants import REPO_LOCAL_PATH

# %% Load case file
AGORA_CASE_FILE = os.path.join(REPO_LOCAL_PATH, "case_agora", "city_a.csv")

data = pandas.read_csv(AGORA_CASE_FILE)

# %% PLot data rslt

plt.plot(float(list(data["ADR_USD"])))
