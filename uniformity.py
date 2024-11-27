import os

datasets = {
    "quechua" : {
        "1.0.0" : "quechua_1_0_0.py"
    },
}

def load_dataset(name: str, version: str, dst : str = ".") -> None:
    if not name in datasets.keys():
        raise ValueError(f"There is no dataset with the name {name}")
    if not version in datasets[name].keys():
        raise ValueError(f"The dataset with the name {name} doesn't have a version {version}")
    script = __import__(datasets[name][version])

    os.makedirs(dst)

    script.load_to(dst)
