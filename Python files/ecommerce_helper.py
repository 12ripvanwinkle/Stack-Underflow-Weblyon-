import os
import shutil
import re

def copy_image_and_update_css(image_folder, destination_folder, css_file, target_image_name):
    # Get the list of files in the image folder
    image_files = os.listdir(image_folder)
    
    # Check if the target image exists in the folder
    if target_image_name in image_files:
        # Define the source image path
        source_image_path = os.path.join(image_folder, target_image_name)
        
        # Define the destination image path in User_Ecommerce
        destination_image_path = os.path.join(destination_folder, target_image_name)

        # Copy the image to the User_Ecommerce folder
        shutil.copy(source_image_path, destination_image_path)
        print(f"Copied {target_image_name} to {destination_folder}")

        # Read the CSS file to update it
        with open(css_file, 'r', encoding='utf-8') as file:
            css_content = file.read()

        # Use regex to replace the background URL and update the path
        new_css_content = re.sub(
            r'background:\s*url\([^\)]+\);',  # Match any url() in the CSS
            f'background: url({target_image_name});',  # Replace with just the image name
            css_content
        )

        # Write the updated CSS back to the existing Cafestyle.css file
        with open(css_file, 'w', encoding='utf-8') as file:
            file.write(new_css_content)

        print(f"Updated CSS with image: {target_image_name}")
    else:
        print(f"{target_image_name} not found in the specified folder.")

# Specify the folder where images are stored, the destination folder, and the CSS file
image_folder = "Ecommerce_templates/cafe_images"  # Folder where images are stored
destination_folder = "User_Ecommerce"  # Folder where the image and CSS will be copied
css_file = "User_Ecommerce/Cafestyle.css"  # The CSS file to update
target_image_name = "f4b468c720a97521602be6095de1abec.jpg"  # The specific image to use

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Call the function to copy image and update CSS
copy_image_and_update_css(image_folder, destination_folder, css_file, target_image_name)

# gets the review images
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

def review_images_getter(image_files):
    # Take the first 3 images
    selected_images = image_files[:3]

    # Copy them
    for image in selected_images:
        src_path = os.path.join(image_folder, image)
        dst_path = os.path.join(destination_folder, image)
        shutil.copy(src_path, dst_path)
        print(f"Copied {image} to {destination_folder}")
