# knowhow.md — convencion de escritura para agentes

Este archivo es la unica fuente de verdad sobre **como se escribe** una
experiencia en coquitoIA. `FORMAT.md` define los tipos fijos y `AGENTS.md`
es el aviso que se carga al abrir el repo. Todo agente que escriba aca hace
exactamente lo que dice este documento, sin variantes personales.

## 1. Principios

1. `memories.jsonl` manda. Supabase es solo la copia caliente para consultar
   rapido. El archivo guarda TODAS las experiencias.
2. Una experiencia = una linea = un `id` = un `sid`. Nunca dos filas del mismo
   tema; nunca un titulo retocado para disfrazar una gemela.
3. Antes de escribir, buscar. Si la entrada existe, editarla; si no, crearla.
4. Verificar ejecutando: comando, hash, endpoint o archivo real. Lo que no se
   pudo verificar se dice explicitamente, no se afirma.
5. Sin secretos, claves, tokens ni datos personales. La clave publishable de
   Supabase va en la variable de entorno `COQUITO_SUPABASE_KEY`.
6. Escribir para un agente que no vio el chat: la linea debe bastarse sola.

## 2. Elegir `k`

| `k` | Se usa cuando | Ejemplo |
| --- | --- | --- |
| `doctrine` | Es una regla de como trabajar, valida siempre y en mas de un proyecto. | "Sin SSE indexado en BinASM" |
| `recipe` | Es un procedimiento repetible con pasos concretos. | "Como regenerar la copia local" |
| `experience` | Es un hallazgo de un proyecto o sesion, con evidencia. | "Crash sin mensaje al llamar user-func" |
| `reference` | Es un dato estable de una herramienta, ruta o API. | "Exports de libspasm-ffmpeg.dll" |

Si una experiencia parece `doctrine` pero solo paso una vez, es `experience`.
Si es `doctrine` pero tiene pasos ordenados, es `recipe`.

## 3. Nombres

- `d` (dominio): minusculas, guiones, corto y estable (`spasm-lang`,
  `nutoys-vst`, `opencode`). No inventar dominios nuevos si existe uno cercano.
- `id`: `<d>/<slug>`. Slug = titulo en ascii minusculo, palabras separadas por
  `-`, maximo 80 caracteres. **Inmutable**: no cambia aunque cambie el titulo.
- `sid`: UUID de Supabase. Para entradas nuevas generarlo con
  `[guid]::NewGuid()` (PowerShell) o `uuid.uuid4()` (Python). **Inmutable**.
- `t`: una linea, descriptiva, empieza por el tema concreto, no por "Como...".
  Unico dentro del dominio. Con acentos esta bien; el slug no los lleva.

## 4. Redaccion campo por campo

| Campo | Que va | Que no va |
| --- | --- | --- |
| `s` | 1-3 frases: que pasa o que es y por que importa. | Cronologia, "hoy", opinion. |
| `sol` | La regla o los pasos numerados. Comandos y rutas reales. | Explicaciones largas, posibilidades no probadas. |
| `less` | Una leccion generalizable y su razon. | Repetir `s` con otras palabras. |
| `src` | Ruta absoluta del archivo donde se verifico. | Rutas imaginadas. Si no hay archivo, omitir y poner la evidencia en `sol`. |
| `tags` | 3-6 etiquetas minusculas en ascii slug, ordenadas. Solo las que clasifican de verdad. | Tags de una sola entrada, mayusculas, sinopsis. |
| `at` | Fecha `AAAA-MM-DD` en que se verifico el hallazgo. | La fecha de hoy por costumbre. |
| `imp` | Importancia segun la escala de abajo. | Inflar todo a 9-10. |

Escala de `imp`:

- **10**: regla canonica que cambia como se trabaja en varias areas.
- **8-9**: gotcha verificado con consecuencia real (crash, build roto, dato perdido).
- **6-7**: receta o dato que ahorra tiempo de forma repetida.
- **4-5**: referencia util.
- **1-3**: nota de contexto.

Reglas de estilo:

- Español en el contenido; identificadores, comandos, rutas y nombres de
  herramientas tal cual estan.
- Texto plano de una sola linea por campo. Sin markdown, sin emojis, sin saltos
  de linea dentro del valor.
- Sin "yo", "aprendi", "ayer", "hoy". La entrada describe el conocimiento, no
  la sesion.
- Una idea por campo. Si `less` repite `s`, borrar `less`.
- Toda afirmacion fuerte lleva evidencia verificable en `sol` o `src`.
- Nunca presentar una inferencia como hecho.

## 5. Plantilla

Copiar, rellenar y **borrar las claves que queden vacias** (nunca `null`). El
orden de claves es fijo:

```json
{"id":"<dominio>/<slug>","sid":"<uuid-v4>","k":"<doctrine|recipe|experience|reference>","d":"<dominio>","imp":<1-10>,"t":"<titulo>","s":"<resumen>","sol":"<solucion>","less":"<leccion>","src":"<ruta>","tags":["<tag>","<tag>"],"at":"AAAA-MM-DD"}
```

Para editar una entrada existente: mantener `id` y `sid`, cambiar solo los
campos que el resultado real contradice.

## 6. Flujo obligatorio

Una experiencia = un commit. No se guarda nada sin pasar por estos pasos.

1. Buscar: `python tools/check.py` y leer `index.jsonl` por `d`, `k` o titulo.
2. Escribir o editar la linea en `memories.jsonl` con la convencion de arriba.
3. Regenerar el indice y validar: `python tools/check.py --reindex` debe
   imprimir `OK`.
4. Espejar: `powershell tools/mirror.ps1 -Only <id>` (sin `-Only` para todo).
   Si falla, se commitea igual y se avisa: manda el archivo.
5. Commitear `memories.jsonl` e `index.jsonl` juntos. Asunto `Area: resumen`
   en español sin tildes; cuerpo explica el por que, no repite el diff.
6. `git push origin main`.
7. Verificar por hash con `git ls-remote`, no por el mensaje de exito.

## 7. Checklist antes de commitear

- [ ] Busque primero y no hay gemelas ni titulos repetidos en el dominio.
- [ ] `id` y `sid` son estables; `sid` es un UUID valido.
- [ ] Claves en orden fijo; campos vacios omitidos, nunca `null`.
- [ ] `k` y `imp` elegidos con las reglas de arriba.
- [ ] El contenido se entiende sin el chat; una idea por campo; sin secretos.
- [ ] `python tools/check.py --reindex` imprime `OK`.
- [ ] Espejo ejecutado o fallo avisado.
- [ ] Commit de un solo tema con asunto en español sin tildes.

## 8. Ejemplo de alta

```json
{"id":"opencode/sin-secretos-en-opencode-json","sid":"11111111-1111-4111-8111-111111111111","k":"doctrine","d":"opencode","imp":10,"t":"Claves de proveedor en opencode.json: siempre {env:VAR}","s":"Una clave escrita en claro queda en el historial de sesiones aunque se borre el archivo; borrarla no la invalida.","sol":"1. Poner toda clave como {env:VAR}. 2. Definir la variable fuera del repo. 3. Si ya quedo en claro, rotarla.","less":"Rotar es la unica accion que invalida una clave expuesta: borrar archivos y backups no alcanza.","src":"C:\\Users\\quamagi\\.config\\opencode\\AGENTS.md","tags":["apikey","config","opencode","secretos"],"at":"2026-10-26"}
```
