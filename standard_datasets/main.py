import importlib
import os
from os.path import join

datasets = {
    "quechua" : {
        "1.0.0" : "standard_datasets.quechua.v1_0_0"
    },
}

def load_dataset(
      name: str, 
      version: str,
      dst : str = "."
    ) -> None:

    """
    Args:
      name (str): Name of the dataset
      version (str): Version of dataset, starting from '1.0.0'
      dst (str, optional): directory to load the dataset relative
        to the script which called this function. Defaults to '.'
    
    Returns:
      None
    
    Raises:
      ValueError: if name or version do not exist
    """
    # check if dataset exists
    dataset_exists = name in datasets.keys()
    if not dataset_exists:
        raise ValueError(f"There is no dataset with the name '{name}'")
    
    # check if dataset exists
    version_exists = version in datasets[name].keys()
    if not version_exists:
        raise ValueError(f"The dataset with the name '{name}' doesn't have a version {version}")

    # make directories
    os.makedirs(dst, exist_ok=True)

    # import script and call its load_to function
    module = importlib.import_module(datasets[name][version])
    module.load_to(dst)
