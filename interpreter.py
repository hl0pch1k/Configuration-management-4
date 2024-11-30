import json
import struct
import sys

# Размер памяти виртуальной машины
VM_MEMORY_SIZE = 1024

# Функция интерпретации бинарного файла для выполнения команд УВМ
def interpret(binary_file, result_file):
    # Память виртуальной машины
    memory = [0] * VM_MEMORY_SIZE
    # Регистр аккумулятора
    accumulator = 0

    # Чтение текстового бинарного файла
    with open(binary_file, 'r') as file:
        lines = file.readlines()

    results = []

    # Интерпретация команд
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 3:
            raise ValueError("Неверный формат команды в бинарном файле")

        command_hex, operand_1_str, operand_2_str = parts
        command = int(command_hex, 16)
        operand_1 = int(operand_1_str)
        operand_2 = int(operand_2_str)

        if command == 0xC0:  # LOAD_CONST
            accumulator = operand_1
            results.append({"command": "LOAD_CONST", "value": accumulator})

        elif command == 0xD8:  # LOAD_MEM
            address = operand_1
            if 0 <= address < VM_MEMORY_SIZE:
                accumulator = memory[address]
                results.append({"command": "LOAD_MEM", "address": address, "value": accumulator})
            else:
                raise ValueError(f"Неверный адрес памяти: {address}")

        elif command == 0xDF:  # STORE_MEM
            address = operand_1
            if 0 <= address < VM_MEMORY_SIZE:
                memory[address] = accumulator
                results.append({"command": "STORE_MEM", "address": address, "value": accumulator})
            else:
                raise ValueError(f"Неверный адрес памяти: {address}")

        elif command == 0x1B:  # MIN_OP
            address = operand_1
            if 0 <= address < VM_MEMORY_SIZE:
                accumulator = min(accumulator, memory[address])
                results.append({"command": "MIN_OP", "address": address, "value": accumulator})
            else:
                raise ValueError(f"Неверный адрес памяти: {address}")

        else:
            raise ValueError(f"Неизвестная команда: {command}")

    # Запись результатов в файл в формате JSON
    with open(result_file, 'w') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python interpreter.py <binary_file> <result_file>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]

    interpret(binary_file, result_file)
