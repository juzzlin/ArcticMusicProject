import re

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
            current_song = {'title': stripped_line[1:].strip(), 'links': {}}
        elif ':' in stripped_line and current_song:
            platform, url_with_notes = stripped_line.split(':', 1)
            url = url_with_notes.strip()
            
            # Strip parenthetical notes from the URL
            url = re.sub(r'\s*\(.+?\)', '', url)
            
            if url:
                url = url.replace('https://https://', 'https://')
                current_song['links'][platform.strip()] = url
    
    if current_song:
        songs.append(current_song)
            
    return songs

def generate_html(songs):
    song_list_html = ""
    for song in songs:
        song_list_html += '                <div class="song">\n'
        song_list_html += f"                    <h3>&#128191; {song['title']}</h3>\n"
        song_list_html += '                    <div class="song-links">\n'
        for platform, url in song["links"].items():
            song_list_html += f'                        <a href="{url}" target="_blank">{platform}</a>\n'
        song_list_html += '                    </div>\n'
        song_list_html += '                </div>\n'
    return song_list_html

def inject_html(html_path, new_song_content):
    with open(html_path, "r") as f:
        html_content = f.read()
    
    # This regex finds the song-list div and captures its opening and closing tags.
    # It will replace everything inside the div.
    placeholder_regex = r'(<div class="song-list">)(.*?)(</div>)'
    
    # Use a replacer function for robust replacement
    def replacer(match):
        opening_tag = match.group(1) # <div class="song-list">
        closing_tag = match.group(3) # </div>
        # Rebuild the div with only the new content
        return f"{opening_tag}\n{new_song_content}\n            {closing_tag}"

    # Pass the function as the replacement argument
    updated_html = re.sub(placeholder_regex, replacer, html_content, flags=re.DOTALL)
    
    with open(html_path, "w") as f:
        f.write(updated_html)

# Main execution
songs = parse_songs('BiisienLinkit.txt')
song_html = generate_html(songs)
inject_html('index.html', song_html)

print("parser.py successfully updated the song list in index.html with the correct replacement logic.")
