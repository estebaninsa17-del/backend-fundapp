## Descripción

<!-- Describe brevemente qué cambia este PR y por qué es necesario. -->

## Tipo de cambio

Marca el tipo que aplica:

- [ ] `feat` — Nueva funcionalidad
- [ ] `fix` — Corrección de bug
- [ ] `docs` — Solo documentación
- [ ] `refactor` — Refactorización sin cambio de comportamiento
- [ ] `test` — Pruebas
- [ ] `chore` — Mantenimiento / configuración
- [ ] `ci` — Cambios en CI/CD
- [ ] `perf` — Mejora de rendimiento
- [ ] `build` — Cambios en build o dependencias

## ¿Cómo se probó?

<!-- Describe los pasos que seguiste para verificar el cambio. -->

- [ ] Servidor levantado con `uvicorn app.main:app --reload`
- [ ] Endpoints probados en Swagger (`/docs`) o con cliente HTTP
- [ ] Sin errores en consola / logs

## Checklist de verificación

- [ ] Los commits siguen [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] La rama parte de `develop` (o `main` solo para hotfix)
- [ ] No se modificó código fuera del alcance del PR
- [ ] Se actualizó documentación si aplica
- [ ] `requirements.txt` solo se tocó si era estrictamente necesario

## Issues relacionados

<!-- Ejemplo: Closes #12 -->
