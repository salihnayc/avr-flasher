import os
import subprocess
import sys


if len(sys.argv) > 1:
    if sys.argv[1] in ["help", "--help"]:
        print("USAGE: buildAndFlash.py [file] [board] [port]")
        print("EXAMPLE: buildAndFlash.py blink.c atmega328p COM10")
        exit(0)
    else:
        filePath = sys.argv[1]
        fileName = os.path.basename(filePath).split(".")[0]
        board = sys.argv[2]
        port = sys.argv[3]

    print("Compiling")
    subprocess.run(["avr-gcc", f"-mmcu={board}", "-DF_CPU=16000000UL", "-Os", filePath, "-o", f"{fileName}.elf"])

    print("Converting to hex")
    subprocess.run(["avr-objcopy", "-O", "ihex", "-R", ".eeprom", f"{fileName}.elf", f"{fileName}.hex"])

    print("Flashing")
    subprocess.run(["avrdude", "-p", board, "-c", "arduino", "-P", port, "-b", "115200", "-D", "-U", f"flash:w:{fileName}.hex:i"])
