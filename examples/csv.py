import sys, codecs, re, json

def csv_to_json(path, encoding):
    def separate(line):
        line = line.strip()
        q = ''
        if len(line) >= 2:
            if line[0] == line[-1] == '"':
                q = '"'
            elif line[0] == line[-1] == "'":
                q = "'"
        if q:
            return re.split(q+r'?\s*[,;]\s*'+q+'?', line[1:-1])
        else:
            return re.split(r'[,;]', line)
    def unquote(field):
        field = field.replace('""', '"')
        field = field.replace("''", "'")
        return field
    with codecs.open(path, encoding=encoding) as f:
        fieldnames = [unquote(h) for h in separate(f.readline())]
        rows = []
        for line in f:
            fieldvalues = [unquote(f) for f in separate(line)]
            rows.append(dict(zip(fieldnames, fieldvalues)))
    return rows

if len(sys.argv) < 2:
    print "Usage: csv_to_json.py <csvpath> [<encoding>]"
else:
    csv_path = sys.argv[1]
    csv_encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8'
    csv_rows = csv_to_json(csv_path, csv_encoding)
    print(json.dumps(csv_rows, indent=True))

