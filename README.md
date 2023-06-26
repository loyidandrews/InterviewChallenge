# InterviewChallenge

The code aims to compare each pair of images in the dataset folder to identify and delete duplicate or highly similar images. 

It performs the following steps:

1. Retrieves a list of image files in the dataset folder.
2. Checks if there are any image files in the dataset folder. If not, it logs a message and exits.
3. Creates two folders, essentials_folder and nonessential_folder, if they don't exist.
4. Creates a copy of the dataset_folder named dataset_folder.copy.
5. Iterates through each image file in the dataset folder and compares it with other image files.
For each pair of image files, it performs the following steps:
1. Reads and preprocesses the images using the preprocess_image_change_detection function.
2. Compares the preprocessed images using the compare_frames_change_detection function.
3. If the similarity score is below a threshold (200000), it moves the second file to the nonessential_folder.
4. After comparing all image pairs, it checks if any file was marked as a duplicate. If not, it moves the first file to the essentials_folder.
5. Moves the remaining files directly to the essentials_folder.
6. Logs the status of the file movements.
7. Closes the logger.
   
To use this code, you need to provide the paths for the dataset folder. A log file is generated with a unique name based on the current timestamp for logging the processing details.

Note: The code assumes the availability of the preprocess_image_change_detection and compare_frames_change_detection functions from the imaging_interview.py module, which are used for image preprocessing and comparison.

