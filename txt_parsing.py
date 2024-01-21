# script to parse txt files
import os
import pandas

data_folder = "/Users/allisongrossberg/Desktop/Confocal_Images_for_Analysis_Duplicated/"
subfolders = [f.path for f in os.scandir(data_folder) if f.is_dir()]

for folder in subfolders:
    files = os.listdir(folder+"/text_files/")
    data_dict = {"Folder": [], "Name": [], "Image Size": [], "Laser Transmissivity": [], "PMT Voltage": []}
    for file in files:
        with open(folder+"/text_files/"+file) as f:
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
    df.to_csv(f"{folder}_image_metadata.csv")
        
    
