#!/usr/bin/env python3
"""Fix 3 CWV issues across subpages:
1. Remove duplicate Google Fonts CSS from tour/geo pages (116 pages)
2. Add height="630" to blog hero images (134 pages)
3. Defer Cherehapa loading on subpages (300 pages)
"""
import glob
import re

# 1. Remove Google Fonts CSS link (duplicates local /fonts/lora.css)
gfonts_pattern = re.compile(r'\s*<link[^>]*fonts\.googleapis\.com[^>]*>\s*\n?')
gfonts_files = (
    glob.glob('ekskursiya/*/index.html') +
    glob.glob('en/ekskursiya/*/index.html') +
    glob.glob('tury-*/index.html') +
    glob.glob('en/tours-*/index.html') +
    glob.glob('blog/*/index.html') +
    glob.glob('en/blog/*/index.html')
)

gfonts_count = 0
for f in gfonts_files:
    with open(f, 'r') as fh:
        content = fh.read()
    if 'fonts.googleapis.com' in content:
        new_content = gfonts_pattern.sub('', content)
        if new_content != content:
            with open(f, 'w') as fh:
                fh.write(new_content)
            gfonts_count += 1

print(f"[1] Google Fonts removed: {gfonts_count} pages")

# 2. Add height="630" to blog hero images (width="1200" without height)
blog_files = glob.glob('blog/*/index.html') + glob.glob('en/blog/*/index.html')
height_count = 0
for f in blog_files:
    with open(f, 'r') as fh:
        content = fh.read()
    # Match img with width="1200" but no height attribute
    if 'width="1200"' in content and 'width="1200" height=' not in content:
        new_content = content.replace('width="1200"', 'width="1200" height="630"')
        if new_content != content:
            with open(f, 'w') as fh:
                fh.write(new_content)
            height_count += 1

print(f"[2] Blog hero height added: {height_count} pages")

# 3. Defer Cherehapa on subpages (replace sync with deferred pattern)
cherehapa_sync = re.compile(
    r'<script data-cfasync="false" data-no-defer="1">\s*'
    r'\(function\(\)\{var s=document\.createElement\("script"\);s\.async=1;\s*'
    r's\.src=\'https://emrldtp\.cc/NTM1NTY4\.js\?t=535568\';\s*'
    r'document\.head\.appendChild\(s\)\}\)\(\)\s*'
    r'</script>',
    re.DOTALL
)

cherehapa_deferred = '''<script>
(function(){var loaded=false;function loadCH(){if(loaded)return;loaded=true;
var s=document.createElement("script");s.async=1;
s.src='https://emrldtp.cc/NTM1NTY4.js?t=535568';
document.head.appendChild(s)}
if('requestIdleCallback' in window){requestIdleCallback(loadCH,{timeout:5000})}
else{setTimeout(loadCH,5000)}
['scroll','touchstart','mousemove','click'].forEach(function(e){
document.addEventListener(e,loadCH,{once:true,passive:true})})})()
</script>'''

all_subpages = (
    glob.glob('ekskursiya/*/index.html') +
    glob.glob('en/ekskursiya/*/index.html') +
    glob.glob('tury-*/index.html') +
    glob.glob('en/tours-*/index.html') +
    glob.glob('blog/*/index.html') +
    glob.glob('en/blog/*/index.html') +
    glob.glob('about/index.html') +
    glob.glob('en/about/index.html')
)

ch_count = 0
for f in all_subpages:
    with open(f, 'r') as fh:
        content = fh.read()
    if 'emrldtp.cc' in content and 'data-no-defer="1"' in content:
        new_content = cherehapa_sync.sub(cherehapa_deferred, content)
        if new_content != content:
            with open(f, 'w') as fh:
                fh.write(new_content)
            ch_count += 1

print(f"[3] Cherehapa deferred: {ch_count} pages")
print(f"\nTotal pages modified: {gfonts_count + height_count + ch_count}")
