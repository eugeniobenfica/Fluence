import re

def apply_rules(line, rules):
    for trigger, converter in rules.items():
        if trigger(line):
            line = converter(line)
    return line

def h1_trigger(line):
    return line.startswith('# ')

def h1(line):
    return f'<h1>{line[2:]}</h1>'

def h2_trigger(line):
    return line.startswith('## ')

def h2(line):
    return f'<h2>{line[3:]}</h2>'

def h3_trigger(line):
    return line.startswith('### ')

def h3(line):
    return f'<h3>{line[4:]}</h3>'

def h4_trigger(line):
    return line.startswith('#### ')

def h4(line):
    return f'<h4>{line[5:]}</h4>'

def strong_trigger(line):
    if re.findall(r'\*\*(.*?)\*\*', line):
        return True

def strong(line):
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)

def em_trigger(line):
    if re.findall(r'_([^_]+)_', line):
        return True

def em(line):
    return re.sub(r'_([^_]+)_', r'<em>\1</em>', line)

def inline_code_trigger(line):
    if re.findall(r'`([^`]+)`', line):
        return True

def inline_code(line):
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', line)

def anchor_trigger(line):
    if re.findall(r'\[([^]]+)\]\(([^)]+)\)', line):
        return True

def anchor(line):
    return re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)

def block_code_trigger(line):
    return '```' in line

def block_code(line):
    return re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', line, flags=re.DOTALL)


class Markdown:
    LINE_CONVERT_RULES = {
    'html': {
        h1_trigger: h1,
        h2_trigger: h2,
        h3_trigger: h3,
        h4_trigger: h4,
        strong_trigger: strong,
        inline_code_trigger: inline_code,
        em_trigger: em,
        anchor_trigger: anchor,
        }
    }
    ALL_CONVERT_RULES = {
        'html': {
            block_code_trigger: block_code
        }
    }

    def __init__(self, markdown: str):
        self.content = markdown

    def export(self, export_format: str = 'html'):
        rules = self.LINE_CONVERT_RULES.get(export_format, {})
        lines = self.content.splitlines()
        
        for i, line in enumerate(lines):
            lines[i] = apply_rules(line, rules)

        content = '\n'.join(lines)

        all_rules = self.ALL_CONVERT_RULES.get(export_format, {})
        for trigger, converter in all_rules.items():
            if trigger(content):
                content = converter(content)

        return content

if __name__ == '__main__':
    text = """
# Title
## Title 2
### Title 3
#### Title 4
**teste**
_teste_
`print`
```
this = 'my name'
print(this)
```
[post](http://127.0.0.1:5000/blog/AIs-can-be-bad.)
"""

    mk = Markdown(text)
    print(mk.export())