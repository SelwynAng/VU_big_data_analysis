import numpy as np
import pandas as pd
import multiprocessing as mp

df = pd.DataFrame(np.random.randint(3, 10, size=[5, 2]))

def sum_of_squares(column):
    return round((column ** 2).sum(), 2)

if __name__ == '__main__':
    # Pass each column (as a Series) to the function
    columns = [df[col] for col in df.columns]
    with mp.Pool(4) as pool:
        result = pool.map(sum_of_squares, columns)
    print(result)