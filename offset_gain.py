import pandas as pd
import os

folder = "/Users/allisongrossberg/Desktop/metadata_output/"
files = os.listdir(folder)
final_dict = {
    "Series 0 Name": [], 
    "Detector gain #1": [],
    "Detector gain #2": [], 
    "Detector gain #3": [], 
    "Detector gain #4": [],
    "Detector offset #1": [],
    "Detector offset #2": [], 
    "Detector offset #3": [], 
    "Detector offset #4": []
}
for file in files:
    df = pd.read_csv(folder+file)
    # split first column by space once, keep only second part
    df['Key'] = df['Key'].str.split(' ', 1).str[1]
    # drop first column
    df = df.T
    #make first row column headers
    df.columns = df.iloc[0]
    #drop first row
    df = df[1:]
    #keep columns list
    keep_list = [
        "Series 0 Name", 
        "Detector gain #1",
        "Detector gain #2", 
        "Detector gain #3", 
        "Detector gain #4",
        "Detector offset #1",
        "Detector offset #2", 
        "Detector offset #3", 
        "Detector offset #4",
    ]

    df = df[keep_list]
    # convert to dict with column headers mapped to values
    df_dict = df.to_dict('records')[0]
    #append items to final_dict
    final_dict["Series 0 Name"].append(df_dict["Series 0 Name"])
    final_dict["Detector gain #1"].append(df_dict["Detector gain #1"])
    final_dict["Detector gain #2"].append(df_dict["Detector gain #2"])
    final_dict["Detector gain #3"].append(df_dict["Detector gain #3"])
    final_dict["Detector gain #4"].append(df_dict["Detector gain #4"])
    final_dict["Detector offset #1"].append(df_dict["Detector offset #1"])
    final_dict["Detector offset #2"].append(df_dict["Detector offset #2"])
    final_dict["Detector offset #3"].append(df_dict["Detector offset #3"])
    final_dict["Detector offset #4"].append(df_dict["Detector offset #4"])

final_df = pd.DataFrame(final_dict)
final_df.to_csv("offset_gain_compiled.csv")