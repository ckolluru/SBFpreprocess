import glob
import numpy as np
import os
import tifffile as tiffio
import shutil

def load(inputFolder, processEvery, tilesX, tilesY):

    '''---------------------------------------
    Summary: Save images at specific distance in a dataset generated by MicroManager

    This script takes a folder name as input containing MUSE data.
    Expects the folder to have subfolders with name _1, _2, _3 etc. and continuous.
    Each subfolder will have the TIF image stacks output from MicroManager.
    User picks a color channel to extract, the script will create a new folder called Specific slices xyz and store tif images taken at specific regular intervals there.
    Deletes the sub-folder if it already exists and rewrites.
    ------------------------------------------'''

    '''---------------------------------------
    Inputs
    ------------------------------------------'''
    # Assumes all slices are continuous
    folder_name = 'D:\MUSE_datasets\\151\\'

    # Color channel to save (Red - 0, Green - 1, Blue - 2)
    channel = 1

    # Offset to first image
    offset = 0

    # Save images every x microns
    save_images_every_x_microns = 1000
    '''---------------------------------------
    Inputs
    ------------------------------------------'''


    '''---------------------------------------
    Algorithm
    ------------------------------------------'''
    # Folder to save
    if channel == 0:
        folder_to_save = r'Specific slices red'
    if channel == 1:
        folder_to_save = r'Specific slices green'
    if channel == 2:
        folder_to_save = r'Specific slices blue'    

    if os.path.exists(folder_name + folder_to_save):
        shutil.rmtree(folder_name + folder_to_save)

    os.makedirs(folder_name + folder_to_save)

    # Get a list of all the subfolders in there
    subfolder_list = glob.glob(folder_name + '_*')

    # Image counter
    counter = 0

    # Bytes per image
    bytes_per_image = 12009644

    # Section thickness
    section_thickness = 3

    # Images to skip
    skip = np.floor(save_images_every_x_microns / section_thickness)

    # Loop through all sub-folders
    for i in np.arange(len(subfolder_list)):
        current_subfolder =subfolder_list[i]
        
        filelist = glob.glob(current_subfolder + '\*.tif')
        
        # Loop through all files
        for j in np.arange(len(filelist)): 
            
            stack_size = os.path.getsize(filelist[j])
            num_images = np.floor(stack_size / bytes_per_image)
            
            # Loop through all images in files
            for k in np.arange(num_images):
                
                counter = counter + 1
                
                if counter >= offset and (((counter - offset) % skip) == 0):
                    image = tiffio.imread(filelist[j], key = int(k))
                    
                    tiffio.imwrite(folder_name + folder_to_save + r'\\Image_' + str(int(np.floor((counter- offset) * save_images_every_x_microns) / skip)) + '_microns.tif', image.astype('uint8'))

    '''---------------------------------------
    Algorithm
    ------------------------------------------'''