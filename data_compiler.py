import os
import pandas as pd

data_folder = "/Users/allisongrossberg/Desktop/Test_Output_Folder/"
all_files = os.listdir(data_folder)

dapi_duplicate_image_list = [file for file in all_files if file.endswith("-DAPI_Duplicate_Image_Results.csv")]
gfap_duplicate_image_list = [file for file in all_files if file.endswith("-GFAP_Duplicate_Image_Results.csv")]
gfap_mfi_list = [file for file in all_files if file.endswith("-GFAP_MFI_Results.csv")]
vimentin_mfi_list = [file for file in all_files if file.endswith("-Vimentin_MFI_Results.csv")]
all_mfi_list = gfap_mfi_list + vimentin_mfi_list

dapi_duplicate_df = []
for file in dapi_duplicate_image_list:
    df = pd.read_csv(data_folder + file)
    # drop last row
    df = df[:-1]
    # Set "Count" column equal to its max
    df["Count"] = df["Count"].max()
    # Take the average of all other columns ignore non numeric columns
    df = df.mean(numeric_only=True)
    if not dapi_duplicate_df:
        dapi_duplicate_df = df
    else:
        dapi_duplicate_df = dapi_duplicate_df.append(df, ignore_index=True)

gfap_duplicate_df = []
for file in gfap_duplicate_image_list:
    df = pd.read_csv(data_folder + file)
    # drop last row
    df = df[:-1]
    # Set "Count" column equal to its max
    df["Count"] = df["Count"].max()
    # Take the average of all other columns
    df = df.mean(numeric_only=True)
    if not gfap_duplicate_df:
        gfap_duplicate_df = df
    else:
        gfap_duplicate_df = gfap_duplicate_df.append(df, ignore_index=True)

mfi_df = []
for file in gfap_mfi_list:
    df = pd.read_csv(data_folder + file)
    # Create a new column "Marker" with either "GFAP" or "Vimentin"
    df["Marker"] = "GFAP" if file.endswith("-GFAP_MFI_Results.csv") else "Vimentin"
    if not mfi_df:
        mfi_df = df
    else:
        mfi_df = mfi_df.append(df, ignore_index=True)

