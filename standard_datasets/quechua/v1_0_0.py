import numpy as np
import os
from os.path import join
import pandas as pd
import shutil
from sklearn.utils import shuffle
from urllib.request import urlretrieve

def min_max_scale(x,old_range,new_range):
    out = (x-old_range[0])/(old_range[1]-old_range[0])
    out = out*(new_range[1]-new_range[0])+new_range[0]
    return out

# define maps to normalize labels later on # TODO rephrase comment !!
emotion_names_map={
    'anger':'anger',
    'boredom':'boredom',
    'happy':'happiness',
    'sleepy':'sleepiness',
    'sadness':'sadness',
    'calm':'calmness',
    'fear':'fear',
    'excited':'excitement',
    'neutral':'neutral',
    'angry':'anger',
    'bored':'boredom',
}
age_map = {
    "a1":43,
    "a2":36,
    "a3":49,
    "a4":28,
    "a5":45,
    "a6":36,
}
gender_map = {
    "a1":"female",
    "a2":"male",
    "a3":"female",
    "a4":"male",
    "a5":"female",
    "a6":"male",
}
def load_to_(dst):
  df=pd.DataFrame({"a":"A", "b":"B"}, index=[0])
  save_dir=join(dst,"SAVEDIR")
  os.makedirs(save_dir,exist_ok=True)
  df.to_csv(join(save_dir, "test_DataFrame.csv"))
def load_to(dst) -> None:
    """
    Loads dataset to the specified directory. Also adds train/test split, saves
    all audios in one directory and filters audios with inconsistent labels.

    Args:
        dst (str) : directory where the dataset will be saved
    
    Returns:
        None        
    """
    #################
    # download data #
    #################

    # download zip
    zip_path = join(dst, "download", "zip_files", "quechua.zip")
    if not os.path.exists(zip_path):
        os.makedirs(join(dst, "download", "zip_files"), exist_ok=True)
        urlretrieve("https://figshare.com/ndownloader/files/37361143", zip_path)

    download_dir = join(dst, "download","quechua")
    audio_dir = join(dst, "audios","quechua")

    # unpack zip
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        shutil.unpack_archive(zip_path, download_dir)

    # move audio files to `./audios`
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        src=join(download_dir,"Audios")
        for file in os.listdir(src):
            shutil.copy2(join(src, file) , audio_dir)

    #################
    # create tables #
    #################

    # read `Data` file which contains emotional categories and actors
    data_sheet = pd.read_excel(
        join(dst, "download","quechua","Data","Data","Data.xlsx"),
        sheet_name=None
    )
    df = data_sheet["map"]

    # add dimensional values
    dimensions_df = pd.read_csv(join(dst, "download","quechua","Labels","Labels","Labels.csv"))
    df = df.merge(dimensions_df, on="Audio")

    # drop irrelevant columns
    df.drop(columns=['File', 'Duration (s)'], inplace=True)

    # rename columns
    rename_dict={col:col.lower() for col in df.columns}
    rename_dict["Audio"]="file"
    rename_dict["Actor"]="speaker"
    df.rename(columns=rename_dict, inplace=True)

    # set index
    df["file"]=df["file"].apply(lambda x: join(audio_dir, str(x)+".wav"))
    df.set_index("file", inplace=True)

    # drop files with bad labels
    df=df[df["valence"]!='2.333.333.333'].copy()
    df=df[~df["speaker"].isin(["6-","2_"])].copy()

    # add speaker ages
    df["age"]=df["speaker"].apply(lambda x: age_map[x])

    # add speaker genders
    df["gender"]=df["speaker"].apply(lambda x: gender_map[x])

    # normalize categorical labels TODO rephrase comment !!
    df["emotion"]=df["emotion"].apply(lambda x: emotion_names_map[x]) 

    # normalize dimensional labels
    df["arousal"]=df["arousal"].apply(lambda x: min_max_scale(x,[1,5],[0,1]))
    df["valence"]=df["valence"].apply(lambda x: min_max_scale(float(x),[1,5],[0,1]))
    df["dominance"]=df["dominance"].apply(lambda x: min_max_scale(x,[1,5],[0,1]))

    # create tables dir
    tables_dir = join(dst, "tables")
    # if not os.path.exists(tables_dir):
    os.makedirs(tables_dir, exist_ok=True)

    # save files table
    df.to_csv(join(dst,"tables","quechua_files.csv"))

    ####################
    # train/test split #
    ####################

    dimensions = ["arousal", "valence", "dominance"]
    # select speakers randomly
    speakers = df.speaker.unique()
    np.random.seed(42)
    test_speakers = np.random.choice(speakers, size=2, replace=False)
    train_speakers = [sp for sp in speakers if not sp in test_speakers]

    # shuffle dataframe
    shuffled_df = shuffle(df, random_state=8)

    # split data into train/test dataframes
    test_df = shuffled_df[shuffled_df.speaker.isin(test_speakers)]
    train_df = shuffled_df[shuffled_df.speaker.isin(train_speakers)]

    # save tables as csv
    test_df["emotion"].to_csv(join(dst, "tables","quechua_emotions_test.csv"))
    train_df["emotion"].to_csv(join(dst, "tables","quechua_emotions_train.csv"))
    for dimension in dimensions:
        test_df[dimension].to_csv(join(dst, "tables",f"quechua_{dimension}_test.csv"))
        train_df[dimension].to_csv(join(dst, "tables",f"quechua_{dimension}_train.csv"))
