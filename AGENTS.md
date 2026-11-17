# coquitoIA — aviso para agentes

Repo de memoria para IA. **Leer `knowhow.md` completo antes de escribir**: ahi
esta la convencion obligatoria de redaccion, nombres, espejo y commits.

- Fuente de verdad: `memories.jsonl`. Supabase es la copia caliente; `sid`
  vincula cada linea con su fila.
- Nunca escribir en Supabase directamente ni borrar filas desde aca.
- Toda escritura termina en un commit con `index.jsonl` regenerado y validado.
- Si la experiencia nacio en otro repo, traerla antes con `tools/import.ps1`.
- Sin credenciales en el repo: clave publishable en `COQUITO_SUPABASE_KEY`.

Mapa: `knowhow.md` (procedimiento y convencion) · `FORMAT.md` (tipos y reglas
fisicas) · `index.jsonl` (indice) · `memories.jsonl` (archivo completo).
