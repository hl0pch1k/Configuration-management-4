import os
import subprocess

# Функция для чтения и вывода содержимого бинарного файла
def read_binary_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line.strip())

def run_all():
    # Файлы, которые будут использоваться в процессе
    input_file = 'test_program.asm'
    binary_file = 'output.bin'
    log_file = 'log.json'
    result_file = 'result.json'

    # Шаг 1: Ассемблирование
    print("\n=== Шаг 1: Ассемблирование ===")
    try:
        subprocess.run(['python', 'assembler.py', input_file, binary_file, log_file], check=True)
        print(f"Ассемблирование завершено. Бинарный файл: {binary_file}, Лог-файл: {log_file}")
    except subprocess.CalledProcessError as e:
        print("Ошибка при ассемблировании:", e)
        return

    # Шаг 2: Интерпретация
    print("\n=== Шаг 2: Интерпретация ===")
    try:
        subprocess.run(['python', 'interpreter.py', binary_file, result_file], check=True)
        print(f"Интерпретация завершена. Результат сохранён в: {result_file}")
    except subprocess.CalledProcessError as e:
        print("Ошибка при интерпретации:", e)
        return

    # Шаг 3: Чтение бинарного файла
    print("\n=== Шаг 3: Чтение бинарного файла ===")
    read_binary_file(binary_file)

    print("\n=== Все шаги успешно выполнены ===")

if __name__ == "__main__":
    run_all()