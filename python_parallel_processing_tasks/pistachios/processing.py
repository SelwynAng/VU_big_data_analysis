import os
import zipfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

def extract_zip(zip_path, extract_to="."):
    """
    Unzips a zip file into a specified directory.
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Dataset extracted to: {os.path.abspath(extract_to)}")

def grayscale_image(input_path, output_path):
    """
    Converts an image to grayscale and saves it.
    """
    with Image.open(input_path) as img:
        # "L" means 8-bit pixels, black and white
        gray_img = img.convert("L")
        gray_img.save(output_path)

def process_images_sequential(image_paths, output_dir):
    """
    Processes (grayscale) images sequentially.
    """
    start_time = time.time()
    for img_path in image_paths:
        file_name = os.path.basename(img_path)
        out_path = os.path.join(output_dir, file_name)
        grayscale_image(img_path, out_path)
    end_time = time.time()
    return end_time - start_time

def process_images_parallel(image_paths, output_dir, max_workers=4):
    """
    Processes (grayscale) images in parallel using threads.
    """
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for img_path in image_paths:
            file_name = os.path.basename(img_path)
            out_path = os.path.join(output_dir, file_name)
            futures.append(executor.submit(grayscale_image, img_path, out_path))

        # Wait for all tasks to complete
        for future in as_completed(futures):
            # If an exception occurred in any task, it will be raised here
            future.result()
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    # Extract the ZIP (Adjust paths as needed)
    zip_path = "./downloads/Pistachio_Image_Dataset.zip"
    extract_to = "pistachio_dataset"
    extract_zip(zip_path, extract_to)

    # Collect all image paths
    image_dir = os.path.join(extract_to, "Pistachio_Image_Dataset") 
    # Depending on the zip structure, adjust the folder name inside the ZIP
    all_images = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                all_images.append(os.path.join(root, file))

    # Create output directories
    sequential_output = "output/grayscale_sequential"
    parallel_output = "output/grayscale_parallel"
    os.makedirs(sequential_output, exist_ok=True)
    os.makedirs(parallel_output, exist_ok=True)

    # Process images SEQUENTIALLY
    seq_time = process_images_sequential(all_images, sequential_output)
    print(f"Sequential processing time: {seq_time:.2f} seconds")

    # Process images in PARALLEL
    par_time = process_images_parallel(all_images, parallel_output, max_workers=5)
    print(f"Parallel processing time:   {par_time:.2f} seconds")

    # Compare the speedup
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"Speedup from parallelization ~ {speedup:.2f}x")
