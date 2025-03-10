import os
import shutil
import numpy as np
import tqdm

# Function to copy folder and modify prey.npy and predator.npy
def duplicate_and_modify(folder_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over subfolders
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        # Check if it's a folder
        if os.path.isdir(subfolder_path):
            # Create new folder in output directory
            output_subfolder_path = os.path.join(output_folder, subfolder)
            os.makedirs(output_subfolder_path)

            # Copy all files from source folder to output folder
            for file_name in os.listdir(subfolder_path):
                shutil.copy(os.path.join(subfolder_path, file_name), output_subfolder_path)

            # Modify prey.npy
            prey_path = os.path.join(subfolder_path, "prey.npy")
            if os.path.exists(prey_path):
                prey = np.load(prey_path)
                prey_modified = prey[:, ::1000, :]
                np.save(os.path.join(output_subfolder_path, "prey.npy"), prey_modified)

            # Modify predator.npy
            predator_path = os.path.join(subfolder_path, "predator.npy")
            if os.path.exists(predator_path):
                predator = np.load(predator_path)
                predator_modified = predator[:, ::1000, :]
                np.save(os.path.join(output_subfolder_path, "predator.npy"), predator_modified)
        print("succes")
    print("all_succes")
# Example usage
source_folder = "/Users/oliversange/Desktop/Speed simulations"
output_folder = "/Users/oliversange/Desktop/Compressed simulations/data_equalspeed_r_prey_prey=3r_c_T_A=30_T_0=60_r_prey_pred=3_r_c"

duplicate_and_modify(source_folder, output_folder)