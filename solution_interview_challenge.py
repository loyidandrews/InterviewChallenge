import os
import glob
import cv2
import shutil
import logging
import time
from tqdm import tqdm

#Call image processing functions from the imaging_interview.py
from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection


class ImageProcessor:
    def __init__(self, dataset_folder, essentials_folder, nonessential_folder):
        self.dataset_folder = dataset_folder
        self.essentials_folder = essentials_folder
        self.nonessential_folder = nonessential_folder

    def process_images(self):
        # Get a list of image files in the dataset folder
        imgfiles = []
        for file in glob.glob(os.path.join(self.dataset_folder, "*.png")):
            imgfiles.append(file)

        if not imgfiles:
            logging.info("No files found in the dataset folder. Exiting...")
            return

        # Create the 'essentials' and 'nonessential' folders if they don't exist
        os.makedirs(self.essentials_folder, exist_ok=True)
        os.makedirs(self.nonessential_folder, exist_ok=True)

        # Create a copy of the dataset folder
        shutil.copytree(self.dataset_folder, f"{self.dataset_folder}.copy")

        with tqdm(total=len(imgfiles), desc="Processing Images") as pbar:
            for file1 in imgfiles:
                is_duplicate = False

                for file2 in imgfiles:
                    if file1 == file2:
                        continue
                    # Load the image 1
                    try:
                        if not os.path.exists(file1):
                            raise ValueError(f"File not found: {file1}")

                        img1 = cv2.imread(file1)
                        if img1 is None:
                            raise ValueError(f"Failed to read image: {file1}")

                        gray_image1 = preprocess_image_change_detection(img1)
                        if gray_image1 is None:
                            raise ValueError(f"Failed to preprocess image: {file1}")
                    except Exception as e:
                        logging.error(f"Error processing {file1}: {str(e)}")
                        continue
                    # Load the image 2
                    try:
                        if not os.path.exists(file2):
                            raise ValueError(f"File not found: {file2}")

                        img2 = cv2.imread(file2)
                        if img2 is None:
                            raise ValueError(f"Failed to read image: {file2}")

                        gray_image2 = preprocess_image_change_detection(img2)
                        if gray_image2 is None:
                            raise ValueError(f"Failed to preprocess image: {file2}")
                    except Exception as e:
                        logging.error(f"Error processing {file2}: {str(e)}")
                        continue

                    try:
                        dim = (gray_image1.shape[1], gray_image1.shape[0])
                        gray_image2 = cv2.resize(gray_image2, dim, interpolation=cv2.INTER_AREA)
                        score, _, _ = compare_frames_change_detection(gray_image1, gray_image2, 100)
                    except Exception as e:
                        logging.error(f"Error comparing frames: {str(e)}")
                        continue

                    logging.info(file1)
                    logging.info(file2)
                    logging.info(score)

                    if score < 200000:
                        try:
                            shutil.move(file2, os.path.join(self.nonessential_folder, os.path.basename(file2)))
                            logging.info(f"{file2} was moved to nonessential folder")
                            is_duplicate = True
                        except Exception as e:
                            logging.error(f"Error moving {file2}: {str(e)}")

                    logging.info("================")

                if not is_duplicate:
                    if os.path.exists(file1):
                        try:
                            shutil.move(file1, os.path.join(self.essentials_folder, os.path.basename(file1)))
                            logging.info(f"{file1} was moved to essentials folder")
                        except Exception as e:
                            logging.error(f"Error moving {file1}: {str(e)}")
                    else:
                        logging.info(f"{file1} does not exist or could not be found")

                pbar.update(1)

        # Move the remaining files directly to the essentials folder
        remaining_files = glob.glob(os.path.join(self.dataset_folder, "*.png"))
        if remaining_files:
            with tqdm(total=len(remaining_files), desc="Moving Remaining Files") as pbar:
                for file in remaining_files:
                    if os.path.exists(file):
                        try:
                            shutil.move(file, os.path.join(self.essentials_folder, os.path.basename(file)))
                            logging.info(f"{file} was moved to essentials folder")
                        except Exception as e:
                            logging.error(f"Error moving {file}: {str(e)}")
                    else:
                        logging.info(f"{file} does not exist or could not be found")
                    pbar.update(1)
        else:
            logging.info("No remaining files found in the dataset folder.")

if __name__ == "__main__":
    dataset_folder = "dataset"
    essentials_folder = "essentials"
    nonessential_folder = "nonessential"

    # Generate a unique log file name with timestamp
    log_file = f"image_processor_{time.strftime('%Y%m%d_%H%M%S')}.log"

    # Configure the logger
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    processor = ImageProcessor(dataset_folder, essentials_folder, nonessential_folder)
    processor.process_images()

    # Close the logger
    logging.shutdown()
