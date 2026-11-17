# coquito-ia/1 — especificacion

Formato de memoria legible por maquina. Version 1. Sin contenido para personas.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `memories.jsonl` | Registro completo, una memoria por linea. |
| `index.jsonl` | Proyeccion `id,k,d,imp,t` de `memories.jsonl`, en el mismo orden. |
| `tools/check.py` | Validador, solo stdlib. Imprime `OK` o los errores. |
| `tools/seed.py` | Importador del snapshot inicial. No es sincronizacion. |

## Reglas fisicas

- UTF-8 sin BOM, saltos LF, una linea = un objeto JSON.
- Sin lineas vacias; la ultima linea termina con LF.
- Sin `null`: los campos opcionales vacios se omiten.
- Orden de claves fijo. Orden de filas: `d`, `k`, `id` (ascendente).

## Campos de `memories.jsonl`

| Clave | Tipo | Regla |
| --- | --- | --- |
| `id` | string | `<dominio>/<slug>`, ascii minusculo, guiones. Inmutable. |
| `k` | string | `doctrine`, `recipe`, `experience` o `reference`. |
| `d` | string | Dominio, texto libre minusculo. Igual que el prefijo de `id`. |
| `imp` | int | Importancia 1-10. 8-10 cambia como se trabaja. |
| `t` | string | Titulo, una linea. |
| `s` | string | Resumen. Opcional. |
| `sol` | string | Solucion o procedimiento. Opcional. |
| `less` | string | Leccion aprendida. Opcional. |
| `src` | string | Ruta de origen. Opcional. |
| `tags` | array | Strings minusculos, unicos y ordenados. Opcional. |
| `at` | string | Fecha `AAAA-MM-DD`. Opcional. |

`index.jsonl` usa las mismas claves en este orden: `id,k,d,imp,t`.

## Ejemplo

```json
{"id":"general/no-inventar","k":"doctrine","d":"general","imp":9,"t":"No inventar","s":"Si una capacidad no esta documentada, decirlo."}
```

## Cambios

1. Buscar por `t` o `id`; editar la linea existente.
2. Mantener `id` aunque cambie `t`.
3. Regenerar `index.jsonl`.
4. Correr `python tools/check.py` y solo entonces commitear.
