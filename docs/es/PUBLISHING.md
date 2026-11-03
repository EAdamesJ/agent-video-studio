# Exportación y publicación

Cada render genera MP4, subtítulos SRT/VTT, miniatura, metadatos sociales y el proyecto editable. La publicación directa es opcional; primero muestra requisitos y luego exige confirmación explícita.

## YouTube

1. Crea un cliente OAuth de escritorio en Google Cloud y activa YouTube Data API v3.
2. Configura `YOUTUBE_CLIENT_SECRET_FILE` con la ruta al JSON descargado.
3. Instala `agent-video-studio[youtube]`.
4. Abre un export renderizado, revisa título, descripción y visibilidad y confirma la publicación.

El primer envío abre el flujo local de autorización de Google. La privacidad predeterminada es privada.

## TikTok

Registra una aplicación con Content Posting API, solicita el permiso `video.publish` y define `TIKTOK_ACCESS_TOKEN`. El preflight consulta las opciones de privacidad de la cuenta. Las aplicaciones no auditadas pueden quedar restringidas a publicaciones privadas.

## Instagram Reels

Necesitas una cuenta profesional elegible y permisos de publicación en Meta. Configura `INSTAGRAM_GRAPH_TOKEN`, `INSTAGRAM_ACCOUNT_ID`, `AVS_META_GRAPH_VERSION` y `AVS_PUBLIC_MEDIA_BASE_URL`. El video debe estar disponible en una URL HTTPS pública y directa para los servidores de Meta.

El flujo crea un contenedor Reels, espera su procesamiento y publica el contenedor. Una URL local `localhost` no sirve para este proceso.

## Revisión y reintentos

Preflight muestra credenciales, permisos y requisitos faltantes. Revisa cuenta, plataforma, video, texto y visibilidad antes de marcar la casilla de confirmación. Tras una interrupción de red, comprueba la plataforma antes de reintentar para evitar duplicados.
\n