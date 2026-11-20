# P3 2026/27: material inicial LL(1)

El enunciado completo está en `Enunciado_P3.pdf` y en su fuente editable
`Enunciado_P3.md`. Este paquete contiene el código de los ejercicios 1–4.
Los ficheros LALR se distribuirán después, con las interfaces ya especificadas.

Desde este directorio, con Python 3.10 o posterior:

```bash
python3 -m unittest discover -v
python3 -m unittest -v test_first
python3 -m unittest -v test_ll1_table
```

Completad los cuatro métodos pendientes en `src/grammar.py`. Al principio es normal
que las pruebas fallen con `NotImplementedError`. Podéis añadir métodos auxiliares
y atributos, pero debéis conservar las interfaces y no modificar `src/utils.py`.
No se necesitan dependencias externas para esta primera parte.

Los tests de `test_contracts.py` concretan las convenciones del enunciado; los de
`test_ll1_table.py` comprueban las tablas sin llamar al analizador del ejercicio 1.
Los tests históricos de integración en `test_analyze.py` requieren también E2–E4.
