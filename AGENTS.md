# coquitoIA — contrato para agentes

Memoria de experiencias de trabajo. Texto machine-first: se consulta por indice
y se lee por `id`. Supabase es la copia rapida; el archivo es la verdad.

## Arquitectura (decidida 2026-11-17)

- `memories.jsonl` guarda TODAS las experiencias y es la fuente de verdad.
- Supabase `public.agent_experiences` es la copia caliente: se consulta primero
  cuando hace falta velocidad.
- El espejo solo da de alta y edita. Nunca borres filas en Supabase desde aca.
- Sin credenciales en el repo. La clave publishable va en la variable de entorno
  `COQUITO_SUPABASE_KEY` (valor en `C:\Users\quamagi\opencode-skills\ACCESO.md`).

## Leer

1. Rapido, si hay red: `select id,kind,domain,title,importance from
   public.agent_experiences` filtrando por dominio/tipo.
2. Completo, sin red: `index.jsonl` (`id,sid,k,d,imp,t`), filtrar y abrir solo
   esa linea de `memories.jsonl`.

## Traer lo que quedo solo en Supabase

`powershell tools/import.ps1 [-DryRun]` — baja `agent_experiences`, y **suma**
al archivo solo las filas cuyo `sid` no esta. Nunca pisa ni borra una linea: si
la fila existe, manda el archivo. Corre `seed.py --merge` y `check.py --reindex`
detras. Es el camino cuando una experiencia se guardo desde otro repo
(Supabase primero) y hay que traerla al archivo antes de commitear.

## Escribir: una experiencia = un commit

1. Buscar por `t` o `id`. Si existe, editar esa linea; nunca agregar gemelas.
2. `id` estable: `<dominio>/<slug>`, no cambia aunque cambie el titulo.
   `sid` es el UUID de Supabase: inmutable; para entradas nuevas generar UUID v4.
3. Claves en orden fijo: `id,sid,k,d,imp,t,s,sol,less,src,tags,at`. Vacio se
   omite, nunca `null`. `imp` 1-10, `tags` minusculos unicos y ordenados.
4. Regenerar el indice y validar: `python tools/check.py --reindex` debe imprimir
   `OK`.
5. Espejar: `powershell tools/mirror.ps1 -Only <id>` (o sin `-Only` para todo).
6. Commitear los dos `.jsonl` juntos. Asunto `Area: resumen` en espanol sin
   tildes; el cuerpo explica el por que. Push a `main`.
7. Si el espejo falla, se commitea igual y se avisa: manda el archivo.
8. Una experiencia nueva que nace en otro repo entra por `tools/import.ps1` y
   **viaja en el mismo commit que el trabajo que la produjo** cuando ese repo
   tiene git; si no, se commitea sola aca con el porque en el cuerpo.

Especificacion completa: `FORMAT.md`.
