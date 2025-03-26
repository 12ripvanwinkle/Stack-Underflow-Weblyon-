import shutil
import os

def tester():
    print("Cafe Website")


    # Define the source and destination paths
    source_file = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Cafestyle.css"
    destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Ecommerce"

    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the single file
    shutil.copy(source_file, destination_folder)

    # Define the source and destination for the folder
    source_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\cafe_images"
    destination_images_folder = os.path.join(destination_folder, "cafe_images")  # Ensure correct destination

    # Remove the existing destination folder if it already exists
    if os.path.exists(destination_images_folder):
        shutil.rmtree(destination_images_folder)

    # Copy the entire 'cafe_images' folder
    shutil.copytree(source_folder, destination_images_folder)

    print(f"Folder copied successfully from '{source_folder}' to '{destination_images_folder}'.")

if __name__ == "__main__":
    tester()