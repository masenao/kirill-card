#!/usr/bin/env python3
"""
Деплой визитки на GitHub Pages.

Использование:
    python deploy.py <GITHUB_TOKEN> [имя-репозитория]

Токен можно взять тут: https://github.com/settings/tokens
Нужен классический токен с галочкой "repo" (или fine-grained с правом
Contents: Read and write + Pages: Read and write + Administration: Read and write).

Скрипт сам: создаст репозиторий, зальёт файлы, включит GitHub Pages
и напечатает готовую ссылку на сайт.
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

# Чтобы русский текст нормально печатался в консоли Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API = "https://api.github.com"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = "kirill-card"


def api(method, path, token=None, payload=None):
    """Запрос к GitHub API. Возвращает (код, распарсенный json)."""
    url = API + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "kirill-card-deploy")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return e.code, parsed
    except urllib.error.URLError as e:
        print("Ошибка сети: не удалось связаться с GitHub:", e.reason)
        sys.exit(1)


def git(*args, token=None):
    """Запуск git-команды в папке проекта."""
    cmd = ["git", *args]
    result = subprocess.run(
        cmd, cwd=PROJECT_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        shown = [a for a in args if token not in a] if token else list(args)
        print("git " + " ".join(shown) + " — ошибка:")
        print((result.stderr or result.stdout).strip())
        sys.exit(1)
    return result.stdout.strip()


def main():
    args = sys.argv[1:]
    env_token = os.environ.get("GITHUB_TOKEN", "").strip()

    if env_token:
        # Токен пришёл из переменной окружения — все аргументы это имя репозитория
        token = env_token
        repo = args[0].strip() if args else DEFAULT_REPO
    else:
        if not args:
            print(__doc__)
            print("Не хватает токена. Пример:")
            print("    python deploy.py ghp_xxxxxxxxxxxxxxxx")
            sys.exit(1)
        token = args[0].strip()
        repo = args[1].strip() if len(args) > 1 else DEFAULT_REPO

    print("→ Проверяю токен и узнаю логин...")
    status, user = api("GET", "/user", token)
    if status != 200:
        print("Токен не подошёл (код %s): %s" % (status, user.get("message", "")))
        sys.exit(1)

    login = user["login"]
    print("  Аккаунт: %s" % login)

    print("→ Создаю репозиторий %s/%s ..." % (login, repo))
    status, res = api(
        "POST",
        "/user/repos",
        token,
        {
            "name": repo,
            "description": "Персональный сайт-визитка",
            "private": False,
            "has_issues": False,
            "has_wiki": False,
        },
    )
    if status == 201:
        print("  Репозиторий создан.")
    elif status == 422:
        print("  Репозиторий уже существует — обновляю содержимое.")
    else:
        print("Не удалось создать репозиторий (код %s): %s" % (status, res.get("message", "")))
        sys.exit(1)

    remote = "https://%s:%s@github.com/%s/%s.git" % (login, token, login, repo)

    print("→ Заливаю файлы...")
    subprocess.run(
        ["git", "remote", "remove", "origin"],
        cwd=PROJECT_DIR, capture_output=True, text=True,
    )
    git("remote", "add", "origin", remote, token=token)
    git("add", "-A")
    subprocess.run(
        ["git", "commit", "-m", "Обновление сайта-визитки"],
        cwd=PROJECT_DIR, capture_output=True, text=True,
    )
    git("branch", "-M", "main")
    git("push", "-u", "origin", "main", "--force", token=token)
    print("  Файлы загружены.")

    print("→ Включаю GitHub Pages...")
    status, res = api(
        "POST",
        "/repos/%s/%s/pages" % (login, repo),
        token,
        {"source": {"branch": "main", "path": "/"}},
    )
    if status in (201, 204):
        print("  Pages включён.")
    elif status == 409:
        api(
            "PUT",
            "/repos/%s/%s/pages" % (login, repo),
            token,
            {"source": {"branch": "main", "path": "/"}},
        )
        print("  Pages уже был включён — настройки обновлены.")
    else:
        print("  Предупреждение (код %s): %s" % (status, res.get("message", "")))
        print("  Страницы можно включить вручную: Settings → Pages → Branch: main")

    url = "https://%s.github.io/%s/" % (login, repo)
    print("")
    print("=" * 52)
    print("  ГОТОВО! Сайт будет доступен через 1-2 минуты:")
    print("  " + url)
    print("=" * 52)
    print("")
    print("  Репозиторий: https://github.com/%s/%s" % (login, repo))
    print("  Дальше обновить сайт можно так: git add -A; git commit -m \"правки\"; git push")


if __name__ == "__main__":
    main()

