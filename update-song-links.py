import re
import os
from PIL import Image
from datetime import datetime

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
            current_song = {'title': stripped_line[1:].strip(), 'links': {}, 'image': None, 'date': None, 'skip': False}
        elif stripped_line == '!SKIP' and current_song:
            current_song['skip'] = True
        elif stripped_line.startswith('!IMAGE:') and current_song:
            image_path = stripped_line.replace('!IMAGE:', '').strip()
            current_song['image'] = image_path
            try:
                mod_time = os.path.getmtime(image_path)
                current_song['date'] = datetime.fromtimestamp(mod_time).strftime('%b %Y')
            except FileNotFoundError:
                print(f"Warning: Image file not found for date extraction: {image_path}")
                current_song['date'] = None
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
        if song.get('skip', False):
            continue # Skip this song if the skip flag is True

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
        song_list_html_lines.append('                        <div class="song-header">')
        song_list_html_lines.append(f"                            <h3>{song['title']}</h3>")
        if song['date']:
            song_list_html_lines.append(f"                            <span class=\"song-date\">{song['date']}</span>")
        song_list_html_lines.append('                        </div>')
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

    start_marker = "<!-- SONG_LIST_START -->"
    end_marker = "<!-- SONG_LIST_END -->"
    
    placeholder_regex = re.compile(f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", re.DOTALL)

    def replacer(match):
        return f"{match.group(1)}\n{new_song_content}\n            {match.group(3)}"

    if not placeholder_regex.search(html_content):
         print(f"Error: Could not find '{start_marker}' and '{end_marker}' in {html_path}.")
         return
         
    updated_html = placeholder_regex.sub(replacer, html_content)
    
    with open(html_path, "w") as f:
        f.write(updated_html)

# Main execution
songs = parse_songs('BiisienLinkit.txt')
song_html = process_and_generate_html(songs)
inject_html_with_markers('index.html', song_html)

print("update-song-links.py successfully updated the song list, respecting !SKIP directives.")
