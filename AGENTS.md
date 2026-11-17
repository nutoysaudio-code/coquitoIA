# coquitoIA — contrato para agentes

Memoria de experiencia para modelos de IA. Texto machine-first: se consulta con
`index.jsonl` y se lee por `id` en `memories.jsonl`. No es prosa para personas.

## Estado

- Fuente: snapshot unico de `public.agent_experiences` del 2026-11-17.
- Este repo NO sincroniza con Supabase. No escribas en la base desde aca.

## Leer

1. `index.jsonl`: una linea por memoria con `id,k,d,imp,t`. Filtra por `d`
   (dominio) o `k` (tipo) y ordena por `imp` descendente.
2. Con el `id`, lee esa linea en `memories.jsonl`, que tiene
   `id,k,d,imp,t,s,sol,less,src,tags,at`.
3. Sentido: `s`=resumen, `sol`=solucion, `less`=leccion aprendida,
   `src`=archivo de origen, `tags`=etiquetas, `at`=fecha.

## Escribir

- Busca primero por titulo o por `id`. Si existe, edita esa linea; no agregues
  gemelas.
- `id` estable: `<dominio>/<slug>`. No lo cambies aunque cambie el titulo.
- Una linea JSON por memoria, claves en ese orden fijo. Campos vacios se omiten,
  nunca `null`.
- Ordena por `d,k,id`. `tags` unicos, en minusculas y ordenados. `imp` entre 1 y 10.
- Regenera `index.jsonl` con solo `id,k,d,imp,t`.
- Valida con `python tools/check.py`: debe imprimir `OK`. No commitees si falla.
- Commits: asunto `Area: resumen` en espanol sin tildes; el cuerpo explica el
  por que, no repite el diff. Un tema por commit.
- Prohibido: secretos, claves, tokens y credenciales en URLs.

Especificacion completa: `FORMAT.md`.
