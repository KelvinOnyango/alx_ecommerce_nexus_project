import requests
import os

def download_images(base_url, output_dir, count):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(1, count + 1):
        image_url = f"{base_url}/{i}.jpg"
        response = requests.get(image_url)

        if response.status_code == 200:
            with open(os.path.join(output_dir, f"image_{i}.jpg"), "wb") as file:
                file.write(response.content)
                print(f"Downloaded image {i}")
        else:
            print(f"Failed to download image {i}: {response.status_code}")

if __name__ == "__main__":
    BASE_URL = "https://picsum.photos/id"
    OUTPUT_DIR = "images"
    COUNT = 100

    download_images(BASE_URL, OUTPUT_DIR, COUNT)
