# Ассемблер: переводит команды из текстового файла в текстовый формат, который затем можно интерпретировать.

import json
import sys

# Константы для команд
COMMANDS = {
    "LOAD_CONST": "C0",  # Загрузка константы в аккумулятор
    "LOAD_MEM": "D8",    # Чтение значения из памяти
    "STORE_MEM": "DF",   # Запись значения в память
    "MIN_OP": "1B"       # Бинарная операция MIN
}

# Функция ассемблирования
def assemble(input_file, output_file, log_file):
    # Чтение исходного текстового файла
    with open(input_file, 'r') as file:
        lines = file.readlines()

    assembled_lines = []
    log_entries = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            # Пропуск пустых строк и комментариев
            continue

        parts = line.split()
        command = parts[0]
        args = list(map(int, parts[1:]))

        if command in COMMANDS:
            opcode = COMMANDS[command]
            operand_1 = args[0] if len(args) > 0 else 0
            operand_2 = 0  # Второй операнд всегда 0 в нашем случае

            # Записываем строку в текстовом формате
            assembled_line = f"{opcode} {operand_1} {operand_2}"
            assembled_lines.append(assembled_line)

            # Добавляем лог
            log_entry = {
                "command": command,
                "operand_1": operand_1,
                "operand_2": operand_2
            }
            log_entries.append(log_entry)
        else:
            raise ValueError(f"Неизвестная команда: {command}")

    # Запись в бинарный файл в читаемом формате
    with open(output_file, 'w') as file:
        for line in assembled_lines:
            file.write(line + "\n")

    # Запись лог-файла в формате JSON
    with open(log_file, 'w') as file:
        json.dump(log_entries, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble(input_file, output_file, log_file)