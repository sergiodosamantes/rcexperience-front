import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<a href="mailto:soporte@rc-experience.com.mx">', '<a href="index.html#contacto">')
    content = content.replace('<a class="mailto" href="mailto:elcorreoquequieres@correo.com">', '<a class="mailto" href="index.html#contacto">')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {file}')
