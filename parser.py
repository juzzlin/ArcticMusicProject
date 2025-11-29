import re

def parse_songs(file_path):
    with open(file_path, "r") as f:
        content = f.read().strip()
    
    songs = []
    song_blocks = re.findall(r'^(# .*?)\n(.*?)(?=\n# |\Z)', content, re.MULTILINE | re.DOTALL)
    
    for title_line, link_block in song_blocks:
        song_title = title_line[1:].strip() # Remove the # and strip whitespace
        links = {}
        
        for line in link_block.strip().split('\n'):
            line = line.strip()
            if ':' in line:
                platform, url_with_notes = line.split(':', 1)
                url = url_with_notes.strip()

                # Strip parenthetical notes from the URL
                url = re.sub(r'\s*\(.+?\)', '', url)

                if url:
                    url = url.replace('https://https://', 'https://') 
                    links[platform.strip()] = url
        
        if song_title and links:
            songs.append({'title': song_title, 'links': links})
            
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

def inject_html(html_path, song_html_content):
    with open(html_path, "r") as f:
        html_content = f.read()
    
    # This regex finds the specific injection comment
    placeholder_regex = r'(<!-- Song links will be injected here -->)'
    
    # Replace the placeholder with the generated song HTML
    updated_html = re.sub(placeholder_regex, song_html_content, html_content, flags=re.DOTALL)
    
    with open(html_path, "w") as f:
        f.write(updated_html)

# Main execution
songs = parse_songs('BiisienLinkit.txt')
song_html = generate_html(songs)
inject_html('index.html', song_html)

print("parser.py successfully injected songs into index.html without overwriting other content.")