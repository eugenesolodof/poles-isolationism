import os
import pandas as pd
import rpy2.robjects as ro

from pathlib import Path
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

path_to_rds = PROJECT_ROOT.joinpath('bmodels/fitted')
path_to_csv = PROJECT_ROOT.joinpath('bmodels/converted')

readRDS = ro.r["readRDS"]

for item in os.listdir(path_to_rds):
    filename = os.path.splitext(item)[0]
    path_to_file = (os.path.join(path_to_rds, item))

    rdata = readRDS(path_to_file)

    # датафрейм с апостериорными распределениями
    as_draws_df = ro.r("function(x) posterior::as_draws_df(x)")
    draws_r = as_draws_df(rdata)
    with localconverter(pandas2ri.converter):
        draws_df = pandas2ri.rpy2py(draws_r)

    draws_df.to_csv(os.path.join(path_to_csv, f'{filename}.csv'), index=False)