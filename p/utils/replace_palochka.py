"""
replace_palochka.py
Заменяет цифру 1 на кириллическую палочку Ӏ (U+04C0)
только там, где 1 стоит рядом с кириллической буквой.

Использование:
    python replace_palochka.py ПАПКА [--dry-run]

Примеры:
    python replace_palochka.py .               # текущая папка
    python replace_palochka.py ./dahkilgov     # конкретная папка
    python replace_palochka.py . --dry-run     # показать изменения без записи
"""

import re
import sys
from pathlib import Path

CYRILLIC = re.compile(r'(?<=[\u0400-\u04FF])1|1(?=[\u0400-\u04FF])')

def process_file(path: Path, dry_run: bool) -> int:
    text = path.read_text(encoding='utf-8')
    new_text, count = CYRILLIC.subn('Ӏ', text)
    if count == 0:
        return 0
    if dry_run:
        print(f"  [dry-run] {path.name}: {count} замен")
    else:
        path.write_text(new_text, encoding='utf-8')
        print(f"  {path.name}: {count} замен")
    return count

def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    args = [a for a in args if not a.startswith('--')]

    folder = Path(args[0]) if args else Path('.')
    if not folder.is_dir():
        print(f"Ошибка: папка не найдена: {folder}")
        sys.exit(1)

    html_files = sorted(folder.rglob('*.html'))
    if not html_files:
        print("HTML-файлы не найдены.")
        sys.exit(0)

    print(f"{'[dry-run] ' if dry_run else ''}Обрабатываем {len(html_files)} файлов в {folder}/\n")

    total_files = 0
    total_replacements = 0
    for f in html_files:
        count = process_file(f, dry_run)
        if count:
            total_files += 1
            total_replacements += count

    print(f"\nГотово: {total_replacements} замен в {total_files} файлах.")

if __name__ == '__main__':
    main()
