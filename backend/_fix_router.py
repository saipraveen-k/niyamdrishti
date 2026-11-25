
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("app/modules/assistant/router.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Detect broken pattern: line ends with opening quote + newline, followed by blank line, followed by content + closing quote
    if (line.rstrip(chr(10)).rstrip(chr(13)).endswith(chr(34)) 
            and i + 2 < len(lines) 
            and lines[i+1].strip() == ""
            and lines[i+2].startswith("Please respond")):
        # Extract indentation + variable assignment up to the opening quote
        prefix = line.rstrip(chr(10)).rstrip(chr(13))  # e.g. '            lang_instruction = "'
        # Extract the message part from line i+2
        msg = lines[i+2].rstrip(chr(10)).rstrip(chr(13))  # e.g. 'Please respond in Telugu...'
        # Build corrected line using backslash-n as escape (chr(92)+chr(110))
        bsn = chr(92) + "n"
        new_line = prefix + bsn + bsn + msg + chr(10)
        new_lines.append(new_line)
        i += 3
    else:
        new_lines.append(line)
        i += 1

print("New total lines:", len(new_lines))
for j in range(55, min(70, len(new_lines))):
    print(j+1, repr(new_lines[j]))

with open("app/modules/assistant/router.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

import py_compile
try:
    py_compile.compile("app/modules/assistant/router.py", doraise=True)
    print("Syntax OK")
except py_compile.PyCompileError as e:
    print("Still broken:", e)
