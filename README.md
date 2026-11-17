# coquitoIA

Memoria de experiencias de trabajo para modelos de IA. El contenido esta
escrito para ser leido por una IA, no por una persona: `index.jsonl` es el
indice y `memories.jsonl` el registro completo, un objeto JSON por linea.

Formato: `coquito-ia/1`, definido en `FORMAT.md`.
Contrato para agentes: `AGENTS.md` (se carga automaticamente al abrir el repo).

El registro actual es un snapshot unico de `public.agent_experiences` tomado
el 2026-11-17 (138 entradas). Este repositorio es independiente: no sincroniza
con Supabase y no contiene credenciales.

Validar antes de commitear:

```powershell
python tools/check.py
```
