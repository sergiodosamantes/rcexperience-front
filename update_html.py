import os

def update_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    target1 = '<form action="https://formspree.io/f/meeyvwqy" class="et_pb_contact_form clearfix" method="POST">'
    rep1 = '<form id="contact-form" class="et_pb_contact_form clearfix">'

    target2 = '<div class="et_contact_bottom_container">'
    rep2 = '''<div id="form-status" style="margin-bottom: 15px; font-weight: bold;"></div>
<div class="cf-turnstile" data-sitekey="0x4AAAAAAEFhjYqJOBSfvVcM" data-theme="light" style="margin-bottom: 15px;"></div>
<div class="et_contact_bottom_container">'''

    target3 = '</body>'
    rep3 = '''<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    const statusDiv = document.getElementById('form-status');
    
    if (form) {
      form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        statusDiv.textContent = 'Enviando...';
        statusDiv.style.color = '#333';
        
        const formData = new FormData(form);
        const data = {
          nombre: formData.get('et_pb_contact_nombre_0'),
          email: formData.get('email'),
          mensaje: formData.get('et_pb_contact_mensaje_0'),
          'cf-turnstile-response': formData.get('cf-turnstile-response')
        };
        
        if (!data['cf-turnstile-response']) {
          statusDiv.textContent = 'Por favor, completa el desafío de seguridad.';
          statusDiv.style.color = 'red';
          return;
        }

        try {
          const response = await fetch('/api/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });
          
          const result = await response.json();
          
          if (response.ok) {
            statusDiv.textContent = '¡Mensaje enviado exitosamente!';
            statusDiv.style.color = 'green';
            form.reset();
            if (window.turnstile) {
              window.turnstile.reset();
            }
          } else {
            statusDiv.textContent = result.message || 'Error al enviar el mensaje.';
            statusDiv.style.color = 'red';
          }
        } catch (error) {
          statusDiv.textContent = 'Error de conexión. Inténtalo más tarde.';
          statusDiv.style.color = 'red';
        }
      });
    }
  });
</script>
</body>'''

    if target1 not in content:
        print("Target 1 not found!")
    if target2 not in content:
        print("Target 2 not found!")
    if target3 not in content:
        print("Target 3 not found!")

    content = content.replace(target1, rep1)
    content = content.replace(target2, rep2)
    content = content.replace(target3, rep3)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated index.html")

if __name__ == '__main__':
    update_html()
