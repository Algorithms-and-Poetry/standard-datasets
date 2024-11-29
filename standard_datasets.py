import os

datasets = {
    "quechua" : {
        "1.0.0" : "quechua_1_0_0.py"
    },
}

def load_dataset(name: str, version: str, dst : str = ".") -> None:
    dataset_exists = name in datasets.keys()
    version_exists = version in datasets[name].keys()
    
    # check if dataset & version exist
    if not dataset_exists:
        raise ValueError(f"There is no dataset with the name {name}")
    if not version_exists:
        raise ValueError(f"The dataset with the name {name} doesn't have a version {version}")
    
    # make directories
    os.makedirs(dst)

    # import script and call its load_to function
    path_to_script = os.path.join("datasets", datasets[name][version])
    script = __import__()
    script.load_to(dst)
