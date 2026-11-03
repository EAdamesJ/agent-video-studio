# Privacidad y seguridad

Agent Video Studio está diseñado para un operador local. Los proyectos y medios viven en el directorio de datos configurado. La API local escucha en loopback por defecto y la versión 0.1 no incluye autenticación multiusuario.

## Datos

- Los archivos fuente se copian al directorio administrado; los originales no se modifican.
- Las claves se leen desde `.env` o el entorno y no aparecen en las respuestas de estado de proveedores.
- Tokens OAuth se guardan localmente en `credentials/`.
- Las exportaciones eliminan rutas absolutas administradas y credenciales.
- Cada servicio remoto recibe solo la información necesaria para la operación seleccionada; no se cambia de proveedor automáticamente.

## Agentes y publicación

Las herramientas MCP se limitan a operaciones del proyecto. `import_media` acepta rutas dentro de `AVS_DATA_DIR`; FFmpeg recibe argumentos separados y no acepta comandos de shell proporcionados por el usuario. Publicar requiere una confirmación independiente.

## Acceso por red

Mantén `AVS_HOST=127.0.0.1` para uso local. Para acceder remotamente, coloca la aplicación detrás de TLS, autenticación y controles de red. No expongas la API local sin protección. Instagram requiere que el MP4 de exportación esté disponible públicamente por HTTPS, lo que revela ese archivo a cualquier cliente con acceso a la URL durante la publicación.
\n