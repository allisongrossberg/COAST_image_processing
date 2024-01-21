import os
import pandas as pd

data_folder = "/Users/allisongrossberg/Desktop/Test_Output_Folder/"
all_files = os.listdir(data_folder)

dapi_duplicate_image_list = [file for file in all_files if file.endswith("-DAPI_Duplicate_Image_Results.csv")]
gfap_duplicate_image_list = [file for file in all_files if file.endswith("-GFAP_Duplicate_Image_Results.csv")]
gfap_mfi_list = [file for file in all_files if file.endswith("-GFAP_MFI_Results.csv")]
vimentin_mfi_list = [file for file in all_files if file.endswith("-Vimentin_MFI_Results.csv")]
all_mfi_list = gfap_mfi_list + vimentin_mfi_list

dapi_duplicate_dfs = []
for file in dapi_duplicate_image_list:
    df = pd.read_csv(data_folder + file)
    # drop last row
    df = df[:-1]
    # Set "Count" column equal to its max
    df["Count"] = df[" "].max()
    #delete " " column
    df = df.drop(columns=[" "])
    # Take the average of all other columns ignore non numeric columns
    df_means = df.mean(numeric_only=True)
    #convert means back to one row df
    df = pd.DataFrame(df_means).T
    df["file"] = file
    df["folder"] = data_folder
    dapi_duplicate_dfs.append(df)
# concatenate all dataframes
dapi_duplicate_df = pd.concat(dapi_duplicate_dfs)
dapi_duplicate_df.to_csv("dapi_duplicate_df.csv")

gfap_duplicate_dfs = []
for file in gfap_duplicate_image_list:
    df = pd.read_csv(data_folder + file)
    # drop last row
    df = df[:-1]
    # Set "Count" column equal to its max
    df["Count"] = df[" "].max()
    #delete " " column
    df = df.drop(columns=[" "])
    # Take the average of all other columns ignore non numeric columns
    df_means = df.mean(numeric_only=True)
    #convert means back to one row df
    df = pd.DataFrame(df_means).T
    df["file"] = file
    df["folder"] = data_folder
    gfap_duplicate_dfs.append(df)
# concatenate all dataframes
gfap_duplicate_df = pd.concat(gfap_duplicate_dfs)
gfap_duplicate_df.to_csv("gfap_duplicate_df.csv")

mfi_dfs = []
for file in gfap_mfi_list:
    df = pd.read_csv(data_folder + file)
    # Create a new column "Marker" with either "GFAP" or "Vimentin"
    df["Marker"] = "GFAP" if file.endswith("-GFAP_MFI_Results.csv") else "Vimentin"
    mfi_dfs.append(df)
mfi_df = pd.concat(mfi_dfs)
mfi_df.to_csv("mfi_df.csv")

