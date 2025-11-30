import re
import os
from PIL import Image

def parse_songs(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    songs = []
    current_song = None

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue

        if stripped_line.startswith('#'):
            if current_song:
                songs.append(current_song)
            current_song = {'title': stripped_line[1:].strip(), 'links': {}, 'image': None}
        elif stripped_line.startswith('!IMAGE:') and current_song:
            current_song['image'] = stripped_line.replace('!IMAGE:', '').strip()
        elif ':' in stripped_line and current_song:
            platform, url_with_notes = stripped_line.split(':', 1)
            url = url_with_notes.strip()
            
            url = re.sub(r'\s*\(.+?\)', '', url)
            
            if url:
                url = url.replace('https://https://', 'https://')
                current_song['links'][platform.strip()] = url
    
    if current_song:
        songs.append(current_song)
            
    return songs

def process_and_generate_html(songs):
    song_list_html_lines = []
    for song in songs:
        image_path_html = ""
        if song['image']:
            sanitized_title = re.sub(r'[^a-z0-9]+', '-', song['title'].lower()).strip('-')
            cover_dir = os.path.join('assets', 'covers', sanitized_title)
            output_path = os.path.join(cover_dir, 'cover.png')
            os.makedirs(cover_dir, exist_ok=True)
            
            try:
                with Image.open(song['image']) as img:
                    resized_img = img.resize((256, 256))
                    resized_img.save(output_path, 'PNG')
                image_path_html = f'<img src="{output_path}" alt="{song["title"]} Cover Art" class="song-cover">'
            except Exception as e:
                print(f"Warning: Could not process image for {song['title']}. Error: {e}")

        song_list_html_lines.append('                <div class="song">')
        if image_path_html:
            song_list_html_lines.append(f"                    {image_path_html}")
        
        song_list_html_lines.append('                    <div class="song-details">')
        song_list_html_lines.append(f"                        <h3>{song['title']}</h3>")
        song_list_html_lines.append('                        <div class="song-links">')
        for platform, url in song["links"].items():
            song_list_html_lines.append(f'                            <a href="{url}" target="_blank">{platform}</a>')
        song_list_html_lines.append('                        </div>')
        song_list_html_lines.append('                    </div>')
        song_list_html_lines.append('                </div>')
        
    return "\n".join(song_list_html_lines)

def inject_html_with_markers(html_path, new_song_content):
    with open(html_path, "r") as f:
        html_content = f.read()

    start_marker = "<!-- SONG LIST START -->"
    end_marker = "<!-- SONG LIST END -->"
    
    # Regex to find the content between the markers
    placeholder_regex = re.compile(f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", re.DOTALL)

    # Function to perform the replacement
    def replacer(match):
        # Keep the markers, replace the content between them
        return f"{match.group(1)}\n{new_song_content}\n            {match.group(3)}"

    # Check if the markers are found
    if not placeholder_regex.search(html_content):
         print(f"Error: Could not find '{start_marker}' and '{end_marker}' in {html_path}.")
         return
         
    # Perform the replacement
    updated_html = placeholder_regex.sub(replacer, html_content)
    
    with open(html_path, "w") as f:
        f.write(updated_html)

# Main execution
songs = parse_songs('BiisienLinkit.txt')
song_html = process_and_generate_html(songs)
inject_html_with_markers('index.html', song_html)

print("update-song-links.py successfully updated the song list using the marker comments.")
