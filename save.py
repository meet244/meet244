import requests
import re

url = "https://meets-portfolio-a87880.webflow.io/"

response = requests.get(url)
html = response.text

# Save the html file
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html)

# remove comments from the html file using regex
with open("index.html", "r", encoding="utf-8") as file:
    html = file.read()

html = re.sub(r"<!--(.*?)-->", "", html, flags=re.DOTALL)

# remove data-wf-domain
html = re.sub(r'data-wf-domain=".*?"', "", html)

# get link tag from the html file where rel is stylesheet
link_tag = re.search(r'<link.*?rel="stylesheet".*?>', html)
# get link of stylesheet from the link tag
stylesheet_link = re.search(r'href="(.*?)"', link_tag.group(0)).group(1)

# get script tag from the html file where src is javascript
script_tags = re.findall(r'<script.*?</script>', html)
# check if src is present in the script tag
for script_tag in script_tags:
    if 'src' not in script_tag:
        continue
    if 'integrity' in script_tag:
        continue
    script_src = re.search(r'src="(.*?)"', script_tag).group(1)


# download the stylesheet
response = requests.get(stylesheet_link)
stylesheet = response.text
with open("style.css", "w", encoding="utf-8") as file:
    file.write(stylesheet)

# download the javascript
response = requests.get(script_src)
javascript = response.text
with open("script.js", "w", encoding="utf-8") as file:
    file.write(javascript)