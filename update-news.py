import re
from datetime import datetime

def parse_news(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    news_items = []
    current_item = None

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue

        if stripped_line.startswith('#'):
            if current_item:
                news_items.append(current_item)
            current_item = {'title': stripped_line[1:].strip(), 'content': [], 'date': None}
        elif stripped_line.startswith('!DATE:') and current_item:
            date_str = stripped_line.replace('!DATE:', '').strip()
            try:
                dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
                current_item['date'] = dt_obj.strftime('%d %b %Y')
            except ValueError:
                print(f"Warning: Could not parse date for {current_item['title']}: {date_str}")
        elif current_item:
            current_item['content'].append(stripped_line)
    
    if current_item:
        news_items.append(current_item)
            
    return news_items

def generate_html(news_items):
    news_html_lines = []
    for item in news_items:
        news_html_lines.append('                <div class="news-item">') # Outer container
        if item['date']:
            news_html_lines.append(f"                    <span class=\"news-date\">{item['date']}</span>")
        news_html_lines.append('                    <div class="news-content">') # Inner container
        news_html_lines.append(f"                        <h3>{item['title']}</h3>")
        for paragraph in item['content']:
            news_html_lines.append(f"                        <p>{paragraph}</p>")
        news_html_lines.append('                    </div>')
        news_html_lines.append('                </div>')
        
    return "\n".join(news_html_lines)

def inject_html_with_markers(html_path, new_content):
    with open(html_path, "r") as f:
        html_content = f.read()

    start_marker = "<!-- NEWS_LIST_START -->"
    end_marker = "<!-- NEWS_LIST_END -->"
    
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
try:
    news = parse_news('Uutiset.txt')
    news_html = generate_html(news)
    inject_html_with_markers('index.html', news_html)
    print("update-news.py successfully updated the news section with the new date structure.")
except FileNotFoundError:
    print("Warning: Uutiset.txt not found. No news items were added.")
except Exception as e:
    print(f"An error occurred: {e}")