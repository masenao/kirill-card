# Сайт-визитка Кирилла

Персональный сайт-визитка: **Кирилл, 14 лет, backend-разработчик на Python.**

Чистая статика без сборки и зависимостей: HTML + CSS + JavaScript.
Достаточно открыть `index.html` в браузере.

## Файлы

| Файл | Что делает |
|------|-----------|
| `index.html` | Разметка и весь текст сайта |
| `style.css` | Тёмная тема, анимации, адаптив под мобильные |
| `script.js` | Печатающийся текст, появление блоков при скролле, меню, частицы на canvas |
| `deploy.py` | Скрипт публикации на GitHub Pages (Python, без сторонних библиотек) |
| `deploy_local.py` | То же самое, но токен берётся из Windows Credential Manager |
| `.nojekyll` | Нужен GitHub Pages, чтобы Jekyll не трогал статику |
| `netlify.toml` / `vercel.json` | Конфиги на случай деплоя на Netlify или Vercel |

## Как поменять свои данные

Открой `index.html`, найди секцию `<section class="section" id="contacts">`
и подставь свои ссылки вместо заглушек:

```html
href="https://t.me/"        → твоя ссылка на Telegram
@kirill                     → твой ник в Telegram
href="https://github.com/"  → твой профиль GitHub
github.com/kirill           → твой ник на GitHub
kirill@example.com          → твоя почта
```

Проекты в секции `id="projects"` тоже можно заменить на свои.

---

## Публикация на GitHub Pages (бесплатно и навсегда)

Сайт уже опубликован: **https://masenao.github.io/kirill-card/**

### Обновить сайт после правок

Если вход в GitHub уже сохранён в системе (Windows Credential Manager), достаточно:

```powershell
cd kirill-card
python deploy_local.py
```

Скрипт сам возьмёт сохранённый токен, зальёт файлы и обновит GitHub Pages.

### Публикация с нуля на другом аккаунте

#### 1. Создай токен

1. Зайди на https://github.com/settings/tokens
2. Нажми **Generate new token (classic)**
3. Поставь галочки: **repo** и **workflow**
4. Срок действия — лучше 90 дней
5. Скопируй получившуюся строку (она показывается один раз!)

### 2. Запусти скрипт

Открой терминал в этой папке и выполни:

```powershell
python deploy.py ВСТАВЬ_СЮДА_ТОКЕН
```

Скрипт сам:
* создаст репозиторий на GitHub,
* зальёт все файлы,
* включит GitHub Pages,
* напечатает ссылку на твой сайт вида
  `https://ТВОЙ_ЛОГИН.github.io/kirill-card/`

Через 1–2 минуты сайт откроется по этой ссылке в интернете.

### 3. Как обновлять сайт потом

```powershell
git add -A
git commit -m "обновил сайт"
git push
```

Через минуту изменения появятся на сайте.

---

## Альтернатива: Netlify Drop (совсем без терминала)

1. Открой https://app.netlify.com/drop
2. Перетащи папку `kirill-card` прямо в окно браузера
3. Netlify сразу выдаст ссылку вида `https://случайное-имя.netlify.app`

Это самый быстрый способ, но для обновления сайта нужно будет перетаскивать папку заново.
