import re
import os

def find_gallery_images(gallery_dir='assets/gallery'):
    """Finds all image files in the gallery directory."""
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    images = []
    if os.path.isdir(gallery_dir):
        for f in sorted(os.listdir(gallery_dir)):
            if os.path.splitext(f)[1].lower() in supported_extensions:
                images.append(os.path.join(gallery_dir, f))
    return images

def generate_html(image_paths):
    """Generates the HTML for the gallery grid."""
    html_lines = []
    for path in image_paths:
        alt_text = os.path.splitext(os.path.basename(path))[0]
        html_lines.append(f'                <img src="{path}" alt="{alt_text}">')
    return "\n".join(html_lines)

def inject_html_with_markers(html_path, new_content):
    """Injects the generated HTML into the placeholder markers."""
    with open(html_path, "r") as f:
        html_content = f.read()

    start_marker = "<!-- GALLERY_START -->"
    end_marker = "<!-- GALLERY_END -->"
    
    placeholder_regex = re.compile(f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", re.DOTALL)

    def replacer(match):
        return f"{match.group(1)}\n{new_content}\n                {match.group(3)}"

    if not placeholder_regex.search(html_content):
         print(f"Error: Could not find '{start_marker}' and '{end_marker}' in {html_path}.")
         return
         
    updated_html = placeholder_regex.sub(replacer, html_content)
    
    with open(html_path, "w") as f:
        f.write(updated_html)

# Main execution
images = find_gallery_images()
if images:
    gallery_html = generate_html(images)
    inject_html_with_markers('index.html', gallery_html)
    print("update-gallery.py successfully updated the gallery section.")
else:
    print("No images found in assets/gallery/. The gallery section is empty.")

