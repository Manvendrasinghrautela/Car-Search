import pandas as pd
import os
from bing_image_downloader import downloader

# Load your car data
data = pd.read_csv('cleaned_car_data1.csv')

# Ensure the images folder exists
os.makedirs('static/images', exist_ok=True)

for idx, row in data.iterrows():
    brand = row['brand']
    model = row['model']
    query = f"{brand} {model} car"

    # Generate a safe filename
    filename = f"{brand.strip().lower().replace(' ', '_')}_{model.strip().lower().replace(' ', '_').split()[0]}.jpg"

    # Check if image already exists
    filepath = os.path.join('static/images', filename)
    if os.path.exists(filepath):
        print(f"✅ {filename} already exists, skipping...")
        continue

    # Download the image using Bing Image Downloader
    try:
        downloader.download(
            query,
            limit=1,  # Download only 1 image
            output_dir='static',
            adult_filter_off=True,
            force_replace=False,
            timeout=60
        )

        # Move downloaded image to static/images/
        download_dir = os.path.join('static', query)
        if os.path.exists(download_dir):
            downloaded_images = os.listdir(download_dir)
            if downloaded_images:
                downloaded_image_path = os.path.join(download_dir, downloaded_images[0])
                os.rename(downloaded_image_path, filepath)
                os.rmdir(download_dir)  # remove empty folder
                print(f"✅ Downloaded and moved: {filename}")
    except Exception as e:
        print(f"❌ Error downloading image for {query}: {e}")

    # Update image filename into the DataFrame
    data.at[idx, 'image'] = filename

# Save updated CSV
data.to_csv('car_data.csv', index=False)
print("✅ All images downloaded and CSV updated!")
