#!/usr/bin/env python3
"""Extract tango creator names from todotango.com/creadores/ and tag posts."""
import re, json, os, glob

# Step 1: Extract creator names from the todotango page
with open('/tmp/todotango_creadores.html', 'r', encoding='utf-8') as f:
    html = f.read()

text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)

start_marker = 'A B C D E F G H I J K L M N O P Q R S T U V W Y Z'
end_marker = 'Mapa del sitio'
start = text.find(start_marker)
end = text.find(end_marker)
names_section = text[start + len(start_marker):end] if start > 0 and end > start else text

# Extract names with "Last, First" pattern
name_pattern = re.findall(r'([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+)*,\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s+[A-ZÁÉÍÓÚÜÑ\s][a-záéíóúüñ]+)*)', names_section)

creators = set()
for n in name_pattern:
    n = n.strip()
    if len(n) > 3 and not re.match(r'^[A-Z]$', n):
        creators.add(n)

# Also extract single-word capitalized names (not part of larger phrases)
single_names = re.findall(r'\b([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]{2,}(?:\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]{2,})?)\b', names_section)
for n in single_names:
    n = n.strip()
    if len(n) > 3 and n not in creators:
        creators.add(n)

# Clean up: remove entries that are clearly not names
filtered = set()
for c in creators:
    if len(c) < 4:
        continue
    if re.match(r'^(El|La|Los|Las|Del|De|Y|O|En|Un|Una|Por|Que|Con|Sin)$', c):
        continue
    # Create normalized versions: "Last, First" and "First Last"
    filtered.add(c)
    # Also add reverse: "First Last"
    if ',' in c:
        parts = c.split(',', 1)
        first = parts[1].strip()
        last = parts[0].strip()
        reversed_name = f"{first} {last}"
        filtered.add(reversed_name)
        # Add just last name
        if len(last) > 3:
            filtered.add(last)
        # Add just first name (if compound)
        first_parts = first.split()
        if len(first_parts) >= 2:
            filtered.add(first)

# Also add short forms
short_forms = set()
for c in filtered:
    words = c.split()
    if len(words) >= 2:
        short_forms.add(words[-1])  # just the last name
        short_forms.add(' '.join(words[:2]))  # first two words

filtered.update(short_forms)

sorted_creators = sorted(filtered)
print(f"Extracted {len(sorted_creators)} creator name forms")

with open('/tmp/todotango_creators.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_creators, f, ensure_ascii=False, indent=2)
print("Saved to /tmp/todotango_creators.json")
