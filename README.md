# coquitoIA

Memoria de experiencias de trabajo para modelos de IA. El contenido esta
escrito para ser leido por una IA, no por una persona: `index.jsonl` es el
indice local y `memories.jsonl` el registro completo, un objeto JSON por linea.

Formato: `coquito-ia/2`, definido en `FORMAT.md`.
Contrato para agentes: `AGENTS.md` (se carga automaticamente al abrir el repo).

## Donde vive cada cosa

- **Archivo completo y fuente de verdad:** `memories.jsonl` (140 entradas,
  snapshot de `public.agent_experiences` Actualizado el 2026-11-17).
- **Consulta rapida:** Supabase `public.agent_experiences`; `sid` en el archivo
  es la columna `id` de la tabla. El espejo solo alta/edita, nunca borra.
- **Indice local sin red:** `index.jsonl` (`id,sid,k,d,imp,t`).

No hay credenciales en el repo: la clave publishable se pasa por la variable de
entorno `COQUITO_SUPABASE_KEY`.

## Comandos

```powershell
python tools/check.py --reindex              # regenera indice y valida
powershell tools/mirror.ps1 -DryRun          # ve cuantas filas se espejearian
powershell tools/mirror.ps1 -Only <id>       # espeja una experiencia
```
