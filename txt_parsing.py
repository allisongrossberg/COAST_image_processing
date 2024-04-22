# script to parse txt files
import os
import pandas

folder = "/Users/allisongrossberg/Desktop/8-IN-PROGRESS-COAST_HA_40x_TLR_Exp_1_Comb_ADE_September_9_23/Tiff_Text_Files"
folder_name = folder.split("/")[-2]

files = os.listdir(folder)
files = [file for file in files if file.endswith(".txt")]
data_dict = {"Folder": [], "Name": [], "Image Size": [], "Laser Transmissivity": [], "PMT Voltage": []}
for file in files:
    with open(os.path.join(folder, file)) as f:
        lines = f.readlines()
        file_dict = {}
        for line in lines:
            if line.split('"')[1] not in file_dict:
                file_dict[line.split('"')[1]] = line.split('"')[3]
            else:
                file_dict[line.split('"')[1]] = file_dict[line.split('"')[1]] + ";" + line.split('"')[3]
        #get keys that are in a list
        key_list = [
            "Name",
            "Image Size",
            "Laser Transmissivity",
            "PMT Voltage",
        ]
        file_dict = {key: file_dict[key] for key in key_list if key in file_dict}
        data_dict["Folder"].append(folder.split("/")[-1])
        data_dict["Name"].append(file_dict["Name"])
        data_dict["Image Size"].append(file_dict["Image Size"])
        data_dict["Laser Transmissivity"].append(file_dict["Laser Transmissivity"])
        data_dict["PMT Voltage"].append(file_dict["PMT Voltage"])

df = pandas.DataFrame(data_dict)
df.to_csv(f"{folder_name}_image_metadata.csv")
        
    
