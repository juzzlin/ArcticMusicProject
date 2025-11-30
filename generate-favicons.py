from PIL import Image
import os

def generate_favicons(source_image_path):
    """
    Generates a set of favicons from a source image.
    """
    favicon_dir = os.path.join('assets', 'favicons')
    os.makedirs(favicon_dir, exist_ok=True)

    sizes = {
        'favicon-16x16.png': (16, 16),
        'favicon-32x32.png': (32, 32),
        'apple-touch-icon.png': (180, 180),
        'android-chrome-192x192.png': (192, 192),
        'android-chrome-512x512.png': (512, 512),
    }

    try:
        with Image.open(source_image_path) as img:
            # Generate standard PNG icons
            for filename, size in sizes.items():
                resized_img = img.resize(size, Image.Resampling.LANCZOS)
                output_path = os.path.join(favicon_dir, filename)
                resized_img.save(output_path, 'PNG')
                print(f"Generated: {output_path}")

            # Generate multi-size favicon.ico
            ico_sizes = [(16, 16), (32, 32), (48, 48)]
            ico_path = os.path.join(favicon_dir, 'favicon.ico')
            img.save(ico_path, 'ICO', sizes=ico_sizes)
            print(f"Generated: {ico_path}")

    except FileNotFoundError:
        print(f"Error: Source image not found at '{source_image_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_logo = 'assets/logo-1200x1200.png'
    generate_favicons(source_logo)
