import re, json
html = open('/tmp/todotango_creadores.html', 'r').read()
links = re.findall(r'/creadores/\d+/([^/\"]+)', html)
names = sorted(set(links))
print(f'Found {len(names)} unique creator slugs')
# Convert slugs to readable names: "anselmo-aieta" -> "Anselmo Aieta"
readable = [l.replace('-', ' ').title() for l in names]
with open('/tmp/todotango_creators_clean.json', 'w', encoding='utf-8') as f:
    json.dump(readable, f, ensure_ascii=False, indent=2)
print(f'Saved {len(readable)} names')
for n in readable[:30]:
    print(f'  {n}')
