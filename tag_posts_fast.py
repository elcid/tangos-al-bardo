#!/usr/bin/env python3
"""Final tagger: use a curated, high-quality list of tango creators for tagging."""
import re, json, os, glob, time

POSTS_DIR = '/opt/projects/tangos-al-bardo/posts'

# Load all extracted names
with open('/tmp/todotango_creators.json', 'r', encoding='utf-8') as f:
    all_raw = json.load(f)

# Curated priority list of well-known tango figures (from todotango + general knowledge)
PRIORITY = [
    # Major composers / musicians
    "Anselmo Aieta", "Francisco Canaro", "Juan D'Arienzo", "Carlos Di Sarli",
    "Osvaldo Pugliese", "Aníbal Troilo", "Astor Piazzolla", "Julio De Caro",
    "Alfredo Gobbi", "Osvaldo Fresedo", "Horacio Salgán", "Mariano Mores",
    "Lucio Demare", "José Basso", "Miguel Caló", "Alfredo De Angelis",
    "Ricardo Tanturi", "Florindo Sassone", "Roberto Firpo", "Pedro Laurenz",
    "Francisco Lomuto", "Enrique Rodríguez", "Edgardo Donato", "Pedro Maffia",
    "Sebastián Piana", "Juan Carlos Cobián", "Enrique Delfino",
    "Agustín Bardi", "Eduardo Arolas", "Ángel Villoldo",
    "Armando Pontier", "Leopoldo Federico", "Julián Plaza", "Raúl Garello",
    "Roberto Pansera", "Héctor Varela", "Jorge Caldara",
    "José Libertella", "Luis Stazo", "Ernesto Baffa",
    "Osmar Maderna", "Orlando Goñi", "Fulvio Salamanca",
    "Vicente Greco", "Francisco Pracánico", "Adolfo Carabelli",
    "Alberto Caracciolo", "Eduardo Del Piano", "Carlos Figari",
    "José Colángelo", "Juan José Mosalini", "Rodolfo Mederos",
    "Domingo Federico", "Alberto Di Paulo",
    
    # Major lyricists / poets
    "Enrique Cadícamo", "Homero Manzi", "Cátulo Castillo", "Enrique Santos Discépolo",
    "Celedonio Flores", "Alfredo Le Pera", "José María Contursi",
    "Pascual Contursi", "Homero Expósito", "Virgilio Expósito",
    "Eladia Blázquez", "Héctor Marcó", "Francisco García Jiménez",
    "Dante Linyera", "Mario Battistella", "José González Castillo",
    "Carlos Bahr", "Enrique Dizeo", "Julio César Sanders", "Luis Bayón Herrera",
    "Luis César Amadori", "Ivo Pelay", "Manuel Romero",
    "Reinaldo Yiso", "Abel Aznar", "José Canet",
    "Luis Rubinstein", "Julio Camilloni", "Abelardo Ferreyra",
    
    # Major singers
    "Carlos Gardel", "Edmundo Rivero", "Julio Sosa", "Roberto Goyeneche",
    "Alberto Castillo", "Ángel Vargas", "Alberto Echagüe", "Roberto Rufino",
    "Francisco Fiorentino", "Héctor Mauré", "Jorge Casal", "Mario Pomar",
    "Alberto Podestá", "Raúl Berón", "Oscar Alonso", "Enrique Campos",
    "Alfredo Belusi", "Jorge Durán", "Tita Merello", "Libertad Lamarque",
    "Nelly Omar", "Ada Falcón", "Azucena Maizani", "Mercedes Simone",
    "Rosita Quiroga", "Hugo del Carril", "Alberto Gómez", "Charlo",
    "Ignacio Corsini", "Agustín Magaldi", "Alberto Marino",
    "Floreal Ruiz", "Ricardo Ruiz", "Jorge Ortiz", "Alberto Morán",
    "Carlos Dante", "Julio Martel", "Alberto Serna", "Néstor Fabián",
    "Roberto Yanés", "José Berón", "Elba Berón", "Raúl Lavié",
    "Guillermo Fernández", "Adriana Varela", "Susana Rinaldi",
    "María Graña", "Lidia Borda", "Ariel Ardit",
    
    # Musicians / instrumentalists
    "Roberto Grela", "Ubaldo De Lío", "Cacho Tirao", "Aníbal Arias",
    "Hugo Díaz", "José Bragato", "Antonio Agri", "Fernando Suárez Paz",
    "Pablo Agri", "Néstor Marconi", "Daniel Binelli", "Juanjo Domínguez",
    "Horacio Malvicino", "Oscar Alemán",
    
    # Dancers / choreographers
    "Juan Carlos Copes", "María Nieves", "Miguel Zotto",
    "Osvaldo Zotto", "Carlos Gavito", "Antonio Todaro",
    "Pepito Avellaneda", "Virulazo", "Elvira Santamaría",
    
    # Key figures / historians
    "José María Otero", "Horacio Ferrer", "Luis Adolfo Sierra",
    "Julián Centeya", "León Benarós",
    
    # More composers/bandleaders
    "Antonio Bonavena", "Joaquín Do Reyes", "Luis Petrucelli",
    "Francisco Rotundo", "Jorge Dragone", "Carlos García",
    "Atilio Stampone", "Vicente Demarco", "Arturo De Bassi",
    "Juan Maglio", "Augusto Berto", "José Martínez",
    "Teófilo Ibáñez", "Ismael Spitalnik", "Raúl Kaplún",
    "Julio Pollero", "Eugenio Nóbile", "Feliciano Brunelli",
    "Manuel Buzón", "Donato Racciatti", "Romeo Gavioli",
    "Mario Demarco", "José Carli", "Víctor Lavallén",
    "Walter Ríos", "Julio Pane",
    
    # Lyricists - more
    "José Rótulo", "Juan Andrés Caruso", "Francisco Gorrindo",
    "Carlos Waiss", "Manuel Meaños", "Lito Bayardo",
]

# Also include ALL names from todotango that have 3+ words (most distinctive)
triple_names = set()
for n in all_raw:
    words = n.split()
    if len(words) >= 3 and len(n) >= 15:
        triple_names.add(n)

# Combine and deduplicate
all_tags = list(dict.fromkeys(PRIORITY + sorted(triple_names)))  # preserve order, dedupe

# Filter out noise
NOISE = {
    'Buenos Aires', 'Argentina', 'Uruguay', 'París', 'Madrid',
    'Francia', 'Italia', 'España', 'Brasil', 'Rusia', 'China', 'Europa',
    'América', 'México', 'Colombia', 'Chile', 'Perú', 'Luna', 'Calle',
}
all_tags = [t for t in all_tags if t not in NOISE]

print(f"Using {len(all_tags)} curated tango creators for tagging")

# Build regex
escaped = [re.escape(c) for c in all_tags]
pattern = re.compile(r'\b(' + '|'.join(escaped) + r')\b', re.IGNORECASE)
name_map = {c.lower(): c for c in all_tags}

tagged = 0
total_tags = 0
tag_counts = {}
files = glob.glob(os.path.join(POSTS_DIR, '*.md'))
t0 = time.time()

for i, fpath in enumerate(files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not fm_match:
        continue
    fm = fm_match.group(1)
    body = fm_match.group(2)
    title_match = re.search(r'title:\s*"([^"]*)"', fm)
    title = title_match.group(1) if title_match else ''
    
    # Clean any previous tags
    fm_cleaned = re.sub(r'\ntags:\s*\[.*?\]', '', fm)
    
    search_text = f"{title}\n{body}"
    matches = pattern.findall(search_text)
    
    matched = set()
    for m in matches:
        original = name_map.get(m.lower(), m)
        matched.add(original)
    
    # Keep top 8 by length
    matched_list = sorted(matched, key=lambda x: -len(x))[:8]
    if not matched_list:
        if 'tags:' in fm:
            new_content = f'---\n{fm_cleaned}\n---\n{body}'
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        continue
    
    yaml_items = []
    for t in matched_list:
        safe = t.replace('\\', '\\\\').replace('"', '\\"')
        yaml_items.append(f'"{safe}"')
    tags_yaml = '[' + ', '.join(yaml_items) + ']'
    
    if 'labels:' in fm_cleaned:
        lines = fm_cleaned.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.strip().startswith('labels:'):
                new_lines.append(f'tags: {tags_yaml}')
        new_fm = '\n'.join(new_lines)
    else:
        new_fm = fm_cleaned + f'\ntags: {tags_yaml}'
    
    new_content = f'---\n{new_fm}\n---\n{body}'
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    for t in matched_list:
        tag_counts[t] = tag_counts.get(t, 0) + 1
    tagged += 1
    total_tags += len(matched_list)
    
    if (i + 1) % 500 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{len(files)} posts ({elapsed:.1f}s)")

elapsed = time.time() - t0
print(f"\nTagged {tagged} posts with {total_tags} total tags in {elapsed:.1f}s")
print(f"Unique tags: {len(tag_counts)}")

top = sorted(tag_counts.items(), key=lambda x: -x[1])[:50]
print("\nTop 50 tags:")
for t, c in top:
    print(f"  {t}: {c}")

with open('/tmp/tag_counts.json', 'w', encoding='utf-8') as f:
    json.dump(tag_counts, f, ensure_ascii=False, indent=2)
print("\nSaved to /tmp/tag_counts.json")
