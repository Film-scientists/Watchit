"""
Some use of pandas
"""
import os
import pandas as pd


data = {"Band": [10, 4, 3],
        "John": [4, 7, 3],
        "Sem": [3, 4, 5],
        "Jam": [2, 2, 2],
        "Bill": [3, 7, 8]}

# Convert from dict to DF
col_names = ["film_1", "Film_2", "Film_3"]
df = pd.DataFrame.from_dict(data, orient="index",
                            columns=col_names)
print("\n", df, "\n")

name = "not_csv.tsv"

# Change format and save
df.to_csv(path_or_buf=name, sep="\t")
new_df = pd.DataFrame()

# Chunk and concat together
for num, chunk in enumerate(pd.read_csv("not_csv.tsv", sep="\t",
                                        chunksize=1,
                                        encoding="UTF-8")):
    print("-" * 20)
    print(f"{num} chunk:")
    print(chunk)
    new_df = pd.concat([new_df, chunk])

print("\nMerged together:\n")
print(new_df)

# Clear directory
# We do not wont leave a mess after running the script
os.remove(name)
