import shutil
import time
from pathlib import Path

def get_fridge_path() -> Path:
    desktop = Path.home() / "Desktop"
    return desktop / "File Fridge"

def create_folder():
    fridge_path = get_fridge_path()
    fridge_path.mkdir(parents=True, exist_ok=True)
    for zone in ["hotbox", "fridge", "freezer"]:
        (fridge_path / zone).mkdir(exist_ok=True)
    print("Заспавнился холодильник для документации :)")

def get_target_zone(file_path: Path) -> str:
    last_modified = file_path.stat().st_mtime
    days_old = (time.time() - last_modified) / (24 * 3600)

    if days_old < 3:
        return "hotbox"
    elif days_old < 14:
        return "fridge"
    else:
        return "freezer"

def move_file(file_path: Path, target_zone: str):
    fridge_path = get_fridge_path()
    target_dir = fridge_path / target_zone
    new_path = target_dir / file_path.name

    counter = 1
    while new_path.exists():
        new_path = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1

    shutil.move(str(file_path), str(new_path))
    print(f"{file_path.name} → {target_zone}")

def sort_files_in_fridge_root():
    fridge_path = get_fridge_path()
    files_moved = 0
    for item in fridge_path.iterdir():
        if not item.is_file():
            continue
        name = item.name.lower()
        if name.startswith("~") or name.endswith((".tmp", ".crdownload", "thumbs.db", ".part")):
            continue

        try:
            zone = get_target_zone(item)
            move_file(item, zone)
            files_moved += 1
        except Exception as e:
            print(f"Ошибка с файлом {item.name}: {e}")

    if files_moved > 0:
        print(f"[{time.strftime('%H:%M')}] Перемещено файлов: {files_moved}")

if __name__ == "__main__":
    create_folder()
    sort_files_in_fridge_root()
    while True:
        try:
            time.sleep(60)
            sort_files_in_fridge_root()
        except KeyboardInterrupt:
            print("\nТы остановил холодильник. Сейчас все испортится...")
            break
