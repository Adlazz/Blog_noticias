# Git Workflow — Blog Noticias

## Estructura de ramas

| Rama | Rol |
|------|-----|
| `main` | Desarrollo. Acá se trabaja y se mergean features. |
| `deploy` | Producción. Railway despliega desde acá. Solo recibe merges desde `main`. |
| `feature/nombre` | Ramas temporales para cada funcionalidad nueva. |

> Nunca commitear directamente en `deploy`. Solo recibe merges.

---

## Flujo de trabajo

### Desarrollo del día a día

```bash
# Asegurate de estar en main actualizado
git checkout main
git pull origin main

# (Opcional) Crear rama de feature para trabajo nuevo
git checkout -b feature/nombre
# ... desarrollás, commiteás ...
git checkout main
git merge feature/nombre
git push origin main
```

### Pasar cambios a producción

```bash
git checkout deploy
git merge main
git push origin deploy
# Railway detecta el push y despliega automáticamente
```

---

## Reglas

1. Nunca hacer `git push --force` en `deploy`.
2. Antes de mergear a `deploy`, verificar que el proyecto corre localmente sin errores.
3. Nunca hacer PR desde GitHub de `deploy` → `main` sin después hacer `git pull origin main` en local.

---

## Comandos útiles

```bash
# Ver estado de todas las ramas
git log --oneline --graph --all

# Ver qué tiene main que deploy no tiene (pendiente de deployar)
git log deploy..main --oneline

# Ver diferencias de código entre ramas
git diff deploy..main
```

---

## Desarrollo local

El proyecto usa un archivo `.env` (ignorado por git) para la configuración local.

```
# .env
DEBUG=True
```

Correr el servidor: `python manage.py runserver`
