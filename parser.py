import re

def parse_songs(file_path):
    with open(file_path, "r") as f:
        content = f.read().strip()
    
    songs = []
    # Regex to find a song block: starts with # Title, followed by links until next # Title or end of file
    # Using re.DOTALL to allow . to match newlines for the links part
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
        song_list_html += f"                    <h3>{song['title']}</h3>\n"
        song_list_html += '                    <div class="song-links">\n'
        for platform, url in song["links"].items():
            song_list_html += f'                        <a href="{url}" target="_blank">{platform}</a>\n'
        song_list_html += '                    </div>\n'
        song_list_html += '                </div>\n'
    return song_list_html

def inject_html(html_path, new_content):
    with open(html_path, "r") as f:
        html_content = f.read()
    
    placeholder_regex = r'(<div class="song-list">)(.*?)(</div>)'
    
    def replace_content(match):
        return f'{match.group(1)}\n{new_content}            {match.group(3)}'

    updated_html = re.sub(placeholder_regex, replace_content, html_content, flags=re.DOTALL)
    
    with open(html_path, "w") as f:
        f.write(updated_html)

# Reset the HTML file to ensure a clean slate, preserving footer links
original_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arctic Music Project</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="hero">
            <h1>Arctic Music Project</h1>
        </div>
    </header>
    <main>
        <section id="about">
            <h2>About Me</h2>
            <p>Welcome to the official website of Arctic Music Project. I am a passionate musician and producer creating sounds inspired by the vast and beautiful landscapes of the north. My music blends electronic elements with organic textures to create a unique and immersive listening experience.</p>
        </section>
        <section id="music">
            <h2>My Music</h2>
            <div class="song-list">
                <!-- Song links will be injected here -->
            </div>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 Arctic Music Project</p>
        <div class="social-links">
            <a href="https://soundcloud.com/arctic-music-project" target="_blank">SoundCloud</a>
            <a href="https://open.spotify.com/artist/YOUR_ARTIST_ID" target="_blank">Spotify</a>
            <a href="https://www.youtube.com/channel/YOUR_CHANNEL_ID" target="_blank">YouTube</a>
        </div>
    </footer>
</body>
</html>
"""
with open('index.html', 'w') as f:
    f.write(original_html)

songs = parse_songs('BiisienLinkit.txt')
song_html = generate_html(songs)
inject_html('index.html', song_html)

print("Final update: Attempting to update the song list in index.html, stripping notes from URLs.")
