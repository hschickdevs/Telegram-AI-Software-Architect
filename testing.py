import subprocess

# Corrected command
command = "touch main.py && echo 'import sys\n\ndef main():\n    if len(sys.argv) != 3:\n        print(\"Usage: python main.py <number1> <number2>\")\n        return\n    number1 = float(sys.argv[1])\n    number2 = float(sys.argv[2])\n    result = number1 + number2\n    print(\"HELLO WORLD! Here is your number: {}\".format(result))\n\nif __name__ == \"__main__\":\n    main()' >> main.py"

# Execute the command to create and write to main.py
subprocess.run(command, shell=True, check=True)
