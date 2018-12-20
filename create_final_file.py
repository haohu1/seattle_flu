import glob, os
import pandas as pd

final_data = pd.concat(map(pd.read_pickle, glob.glob(os.path.join('output/', "infection_individuals_*.pickle"))))
final_data.to_csv("output/infection_individuals.csv")
