import re

with open('LibraryProject/settings.py', 'r') as f:
    content = f.read()

# Remove any existing AUTH_USER_MODEL
lines = content.split('\n')
new_lines = []
for line in lines:
    if 'AUTH_USER_MODEL' not in line:
        new_lines.append(line)

# Add the correct AUTH_USER_MODEL and MEDIA settings
new_lines.append(\"AUTH_USER_MODEL = 'bookshelf.CustomUser'\")
new_lines.append(\"MEDIA_URL = '/media/'\")
new_lines.append(\"MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\")

with open('LibraryProject/settings.py', 'w') as f:
    f.write('\n'.join(new_lines))

print(\"✓ Updated settings.py\")
