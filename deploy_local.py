#!/usr/bin/env python3
"""
Публикация визитки на GitHub Pages.

Берёт токен из Windows Credential Manager (там уже сохранён вход в GitHub),
поэтому вводить его руками не нужно.

Запуск:
    python deploy_local.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def get_token():
    """Достаёт сохранённый токен GitHub через git credential fill."""
    prompt = "protocol=https\nhost=github.com\n\n"
    try:
        result = subprocess.run(
            ["git", "credential", "fill"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as e:
        print("Не удалось обратиться к git: %s" % e)
        return None

    for line in (result.stdout or "").splitlines():
        if line.startswith("password="):
            value = line[len("password="):].strip()
            if value:
                return value
    return None


def main():
    print("-> Ищу сохранённый токен GitHub в Windows Credential Manager...")
    token = get_token()

    if not token:
        print("Токен не найден.")
        print("")
        print("Что делать: создай токен на https://github.com/settings/tokens")
        print("(галочки repo и workflow) и запусти:")
        print("    python deploy.py ТВОЙ_ТОКЕН")
        return 1

    print("   Токен найден, использую его (не показываю).")
    print("")

    env = os.environ.copy()
    env["GITHUB_TOKEN"] = token

    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "deploy.py")],
        cwd=HERE,
        env=env,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
