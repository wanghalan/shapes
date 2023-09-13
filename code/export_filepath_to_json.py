import pathlib
import json
from tqdm import tqdm

if __name__ == "__main__":
    data_files = sorted(pathlib.Path("../data").glob("*.gz"))

    with open("../manifest.json", "w") as f:
        json.dump([str(d)[3:] for d in data_files], f)  # skip initial ../
