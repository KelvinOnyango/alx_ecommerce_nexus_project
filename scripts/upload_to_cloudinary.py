import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

def resize_image(image_path, max_size_mb):
    max_size_bytes = max_size_mb * 1024 * 1024
    if os.path.getsize(image_path) > max_size_bytes:
        with Image.open(image_path) as img:
            img.thumbnail((800, 800))  # Resize to max dimensions
            img.save(image_path, optimize=True, quality=85)
            print(f"Resized {image_path} to fit within {max_size_mb} MB")

def upload_images_to_cloudinary(folder_path, category):
    uploaded_urls = []

    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if os.path.isfile(image_path):
            resize_image(image_path, max_size_mb=10)  # Resize if larger than 10 MB
            response = cloudinary.uploader.upload(
                image_path,
                folder=category,
                use_filename=True,
                unique_filename=False
            )
            uploaded_urls.append({
                "name": image_name,
                "url": response["secure_url"],
                "category": category
            })
            print(f"Uploaded {image_name} to Cloudinary")

    return uploaded_urls

if __name__ == "__main__":
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    FOLDER_PATH = "images"  # Path to the folder containing images
    CATEGORY = "ecommerce"  # Category for the images

    urls = upload_images_to_cloudinary(FOLDER_PATH, CATEGORY)

    # Print URLs for frontend clients
    for url_info in urls:
        print(f"Name: {url_info['name']}, URL: {url_info['url']}, Category: {url_info['category']}")
