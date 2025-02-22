#!/bin/bash
set -e

# Set original dir
ORIGINAL_DIR=$(pwd)
readonly ORIGINAL_DIR

# Set text separator
TEXT_SEPARATOR=$(printf "*%.0s" {1..50})
readonly TEXT_SEPARATOR

# Function for print installation info
print_info() {
  printf "\n%s \n%s \n%s \n\n" "$TEXT_SEPARATOR" "$1" "$TEXT_SEPARATOR"
}

print_info "Оновлення системи та встановлення необхідних пакетів ..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-tk

print_info "Створення тимчасової директорії ..."
BUILD_DIR=$(mktemp -d)
trap 'rm -rf "$BUILD_DIR"' EXIT
cd "$BUILD_DIR"

print_info "Створення віртуального середовища ..."
python3 -m venv venv

print_info "Активація віртуального середовища ..."
source venv/bin/activate

if [ -f "$ORIGINAL_DIR/requirements.txt" ]; then
  print_info "Встановлення залежностей з requirements.txt ..."
  pip install -r "$ORIGINAL_DIR/requirements.txt"
else
  print_info "Відсутній файл requirements.txt..."
  exit 1
fi

print_info "Встановлення PyInstaller ..."
pip install pyinstaller

print_info "Копіювання додатку у тимчасову директорію ..."
cp "$ORIGINAL_DIR"/*.py "$BUILD_DIR"

print_info "Збирання додатку через PyInstaller ..."
pyinstaller --noconsole --onefile app.py

print_info "Копіювання зібраного файлу у /opt/log_generator ..."
sudo rm -rf /opt/log_generator
sudo mkdir -p /opt/log_generator
sudo cp dist/app /opt/log_generator/log_generator
sudo chmod +x /opt/log_generator/log_generator

print_info "Створення ярлика ..."
mkdir -p ~/.local/share/applications
cat >~/.local/share/applications/log_generator.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Log Generator
Comment=Tkinter GUI application
Exec=/opt/log_generator/log_generator
Icon=utilities-terminal
Terminal=false
Categories=Utility;
EOF

print_info "Оновлення кешу ярликів ..."
update-desktop-database ~/.local/share/applications

print_info "Готово! Додаток встановлено."
