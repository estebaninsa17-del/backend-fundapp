# Guía de contribución — FundApp Backend

Este documento describe el flujo de trabajo Git, las convenciones de commits y los pasos para colaborar en el backend FastAPI + Supabase de FundApp.

---

## Ramas (Git Flow)

| Rama | Propósito |
|------|-----------|
| `main` | Producción estable. Solo recibe merges desde `release/*` o `hotfix/*`. |
| `develop` | Integración continua. Base para nuevas funcionalidades. |
| `feature/*` | Nuevas capacidades o mejoras no urgentes. |
| `release/*` | Preparación de versión (QA, bump de versión, changelog). |
| `hotfix/*` | Correcciones urgentes en producción. |

### Convención de nombres

Usa prefijos en kebab-case y nombres descriptivos alineados con los módulos del proyecto:

```
feature/certificados-pdf
feature/actividades-filtro-fecha
fix/auth-token-expirado
hotfix/fix-login-token
release/v1.1.0
chore/setup-git-conventions
```

### Flujo típico

1. Actualiza `develop`: `git checkout develop && git pull origin develop`
2. Crea tu rama: `git checkout -b feature/mi-funcionalidad`
3. Commitea con Conventional Commits (ver abajo).
4. Sube la rama: `git push -u origin feature/mi-funcionalidad`
5. Abre un Pull Request hacia `develop`.
6. Tras revisión y aprobación, se integra en `develop`.
7. Para liberar a producción, se crea `release/vX.Y.Z` desde `develop`, se valida y se mergea a `main`.

### Hotfix en producción

1. `git checkout main && git pull origin main`
2. `git checkout -b hotfix/descripcion-corta`
3. Corrige, commitea, abre PR hacia `main`.
4. Tras el merge, integra también el hotfix en `develop`.

---

## Conventional Commits

Cada commit debe seguir el formato:

```
<type>(<scope>): <descripción en imperativo, minúsculas, sin punto final>
```

### Tipos permitidos

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `refactor` | Refactor sin cambio de comportamiento |
| `test` | Pruebas |
| `chore` | Mantenimiento, tooling, configuración |
| `build` | Build o dependencias de producción |
| `ci` | Pipelines y automatización |
| `perf` | Mejora de rendimiento |

### Scopes sugeridos (módulos del proyecto)

- `auth` — Login, registro, JWT
- `actividades` — CRUD de actividades
- `donaciones` — Registro y consulta de donaciones
- `voluntarios` — Postulaciones y gestión
- `certificados` — Emisión y validación
- `admin` — Estadísticas y panel administrativo
- `core` — Config, seguridad, dependencias compartidas
- `infra` — Repositorios, cliente Supabase
- `deps` — Dependencias
- `ci` — GitHub Actions, hooks

### Ejemplos reales para este proyecto

```
feat(auth): agregar endpoint de refresh token
fix(certificados): corregir validación por documento duplicado
docs(readme): documentar variables de entorno requeridas
refactor(donaciones): extraer lógica de filtrado al servicio
test(voluntarios): agregar pruebas de postulación
chore(deps): actualizar commitizen en requirements-dev
ci(commitlint): validar conventional commits en pull requests
perf(actividades): optimizar consulta de listado paginado
```

### Cuerpo y footer (opcional)

```
feat(admin): agregar endpoint de estadísticas mensuales

Incluye conteo de donaciones y voluntarios activos por mes.

Closes #42
```

---

## Herramientas de desarrollo

### Instalación

```bash
pip install -r requirements-dev.txt
```

### Pre-commit (validación local de mensajes)

Registra el hook una vez por clon del repositorio:

```bash
pre-commit install --hook-type commit-msg
```

A partir de ahí, cada `git commit` validará el mensaje contra Conventional Commits antes de completarse.

### Commitizen

#### Crear commits interactivos

```bash
cz commit
```

#### Verificar mensajes manualmente

```bash
cz check --commit-msg-file .git/COMMIT_EDITMSG
```

#### Bump de versión y changelog

```bash
cz bump
```

Esto actualiza `pyproject.toml`, `CHANGELOG.md` y crea el tag `vX.Y.Z` según los commits desde la última versión.

---

## Pull Requests

- Base: `develop` (salvo hotfix hacia `main`).
- Usa la plantilla de PR en `.github/PULL_REQUEST_TEMPLATE.md`.
- Asegúrate de que todos los commits del PR cumplan Conventional Commits (el workflow `commitlint` lo validará en CI).
- No mezcles cambios de configuración con refactors o features no relacionados.

---

## Reglas importantes

- **No modifiques** `requirements.txt` de producción salvo que el cambio lo exija explícitamente.
- Las dependencias de desarrollo van en `requirements-dev.txt`.
- Mantén los cambios acotados al módulo o tarea del PR.
- Documenta endpoints nuevos o cambios de contrato en el README cuando aplique.

---

## Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)
- [Pre-commit](https://pre-commit.com/)
