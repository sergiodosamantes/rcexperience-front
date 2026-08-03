const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { nombre, email, mensaje, 'cf-turnstile-response': turnstileResponse } = req.body;

  if (!turnstileResponse) {
    return res.status(400).json({ message: 'Se requiere validación anti-spam.' });
  }

  // Verificar el token con Cloudflare Turnstile
  const verifyEndpoint = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
  const secretKey = process.env.TURNSTILE_SECRET_KEY;

  try {
    const turnstileResult = await fetch(verifyEndpoint, {
      method: 'POST',
      body: `secret=${encodeURIComponent(secretKey)}&response=${encodeURIComponent(turnstileResponse)}`,
      headers: {
        'content-type': 'application/x-www-form-urlencoded'
      }
    });
    
    const turnstileData = await turnstileResult.json();
    if (!turnstileData.success) {
      return res.status(400).json({ message: 'La validación anti-spam falló. Inténtalo de nuevo.' });
    }

    // Si Turnstile es válido, enviamos el correo
    const data = await resend.emails.send({
      from: 'Formulario Web <formulario@rc-experience.com.mx>', // Asegúrate de verificar tu dominio en Resend
      to: ['soporte@rc-experience.com.mx'],
      reply_to: email,
      subject: `Nuevo mensaje de ${nombre} - Sitio Web`,
      html: `
        <h2>Nuevo mensaje desde la página web</h2>
        <p><strong>Nombre:</strong> ${nombre}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Mensaje:</strong><br/>${mensaje}</p>
      `,
    });

    res.status(200).json({ message: '¡Mensaje enviado exitosamente!', data });
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({ message: 'Error interno del servidor al procesar tu solicitud.' });
  }
}
