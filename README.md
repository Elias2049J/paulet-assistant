# Paulet Assistant - Backend (Arquitectura Limpia)

Proyecto del curso EFSRT. Este es el backend, el cual implementa caché para respuestas veloces.
Se puede encontrar el frontend aquí: https://github.com/Csalirrosasc/paulet-assistant.git

## Ejemplo de uso del endpoint

### Endpoint principal

`POST /paulet/chat`

**Body esperado:**
```json
{
  "message": "1"
}
```

**Respuesta esperada:**
```json
{
  "respuesta": "Genial! ¿Deseas las notas de este ciclo o de algún otro?\n1. Ciclo en curso\n2. Otro ciclo\n3. Volver a las opciones"
}
```

### Flujo conversacional de ejemplo

1. **Inicio:**
   - Enviar:
     ```json
     { "message": "hola" }
     ```
   - Respuesta:
     ```
     Hola, soy Paulet, tu asistente virtual. Escoge una de las siguientes opciones:
     1. Consultar notas.
     2. Consultar horarios.
     ```

2. **Consultar notas:**
   - Enviar:
     ```json
     { "message": "1" }
     ```
   - Respuesta:
     ```
     Genial! ¿Deseas las notas de este ciclo o de algún otro?
     1. Ciclo en curso
     2. Otro ciclo
     3. Volver a las opciones
     ```

3. **Notas del ciclo actual:**
   - Enviar:
     ```json
     { "message": "1" }
     ```
   - Respuesta:
     ```
     (desde scraping) Notas para usuario_demo en ciclo 2025-1:
     - Matemática: 18 (faltas: 1/5)
     - Física: 19 (faltas: 0/5)
     - Programación: 20 (faltas: 2/5)
     1. Volver a las opciones
     ```

4. **Volver al menú principal:**
   - Enviar:
     ```json
     { "message": "1" }
     ```
   - Respuesta:
     ```
     Hola, soy Paulet, tu asistente virtual. Escoge una de las siguientes opciones:
     1. Consultar notas.
     2. Consultar horarios.
     ```

5. **Consultar horarios:**
   - Enviar:
     ```json
     { "message": "2" }
     ```
   - Respuesta:
     ```
     (desde scraping) Horarios para usuario_demo en ciclo 2025-1:
     Lunes: Matemática 08:00-10:00 Aula 101
     Martes: Física 10:00-12:00 Aula 202
     Miércoles: Programación 14:00-16:00 Aula 303
     1. Volver a las opciones
     ```

## Notas
- El backend está preparado para un solo usuario de pruebas (usuario_demo, clave 123456, ciclo 2025-1).
- El frontend solo debe enviar el campo `message`.
- El flujo conversacional está definido en `decision_tree.json`.
- Los datos de notas y horarios son simulados (hardcoded) para pruebas.
