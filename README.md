# standard-datasets

This project allows you to download opensource dataset, without having 
to worry about **train/test-splits**, **normalizing** numerical features, 
creating **tables** for the data and many more. For an overview of the 
concrete pre-processing steps which were done, please read the individual README for datasets of your interest.

## Installation

Please clone this repository to a directory of your choice. 
Then install the `requirements.txt` as follows:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you use **Powershell**, you can install the requirements like this:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Importing the module:

```python
import sys
sys.path.append("path/to/standard-datasets")
import standard_datasets
```

Please note that the package is spelled with a hyphen (-), while the module
uses an underscore (_).

To download a dataset, pass it's `name`, `version` and optionally a `directory` 
to load the data to. The directory will be created if it 
doesn't already exist. However if the directory exists and already contains
the dataset, it will not be downloaded again and the program will terminate.

## Example

```python
standard_datasets.load_dataset(
    "quechua",
    "1.0.0",
    dst="path/where/the/data/will/be/saved"
)
```

## Datasets

Dataset | Data Description | Size | License | Remarks  
--- | --- | --- | --- | ---
quechua |  **dimensions**: arousal, dominance, valence **emotions**: : happy, sad, bored, fear, sleepy, calm, excited, angry neutral | 3.53GB (12420 audios) |  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | 
subesco |  **emotions**: angry, disgusted, fearful, happy, neutral, sad, surprised | 2.03GB (7000 audios) |  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | 
