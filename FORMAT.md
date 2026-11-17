# coquito-ia/2 — especificacion

Formato de memoria legible por maquina. Version 2: agrega `sid` para espejar
con Supabase. Sin contenido para personas.

La convencion de redaccion, el flujo de trabajo y el checklist viven en
`knowhow.md`, que es la unica fuente de verdad para eso.

## Arquitectura

- `memories.jsonl`: archivo completo, fuente de verdad, una memoria por linea.
- `index.jsonl`: proyeccion `id,sid,k,d,imp,t`, mismo orden. Copia rapida local.
- Supabase `public.agent_experiences`: copia caliente. `sid` = su columna `id`.
- `tools/mirror.ps1`: alta/edicion en Supabase. Nunca borra.
- `tools/check.py`: validador. `tools/seed.py`: importador del snapshot inicial.

## Reglas fisicas

- UTF-8 sin BOM, saltos LF, una linea = un objeto JSON.
- Sin lineas vacias; la ultima linea termina con LF.
- Sin `null`: los campos opcionales vacios se omiten.
- Orden de claves fijo. Orden de filas: `d`, `k`, `id` (ascendente).

## Campos de `memories.jsonl`

| Clave | Tipo | Regla |
| --- | --- | --- |
| `id` | string | `<dominio>/<slug>`, ascii minusculo, guiones. Inmutable. |
| `sid` | string | UUID de Supabase. Inmutable. Unico. |
| `k` | string | `doctrine`, `recipe`, `experience` o `reference`. |
| `d` | string | Dominio minusculo. Igual que el prefijo de `id`. |
| `imp` | int | Importancia 1-10. 8-10 cambia como se trabaja. |
| `t` | string | Titulo, una linea. Unico dentro del dominio. |
| `s` | string | Resumen (en Supabase es `not null`). Opcional. |
| `sol` | string | Solucion o procedimiento. Opcional. |
| `less` | string | Leccion aprendida. Opcional. |
| `src` | string | Ruta de origen. Opcional. |
| `tags` | array | Strings minusculos, unicos y ordenados. Opcional. |
| `at` | string | Fecha `AAAA-MM-DD`. Opcional. |

`index.jsonl` usa las mismas claves en este orden: `id,sid,k,d,imp,t`.

## Ejemplo

```json
{"id":"general/no-inventar","sid":"0bd6cd29-73cf-4c50-bcd7-01a45b30bf2c","k":"doctrine","d":"general","imp":9,"t":"No inventar","s":"Si una capacidad no esta documentada, decirlo."}
```

## Espejo

`powershell tools/mirror.ps1 -Only <id>` hace PATCH si el `sid` ya existe y POST
si no. No envia `created_at` en PATCH: Supabase conserva la fecha original.
Requiere `COQUITO_SUPABASE_KEY`. No hay borrado automatico.

