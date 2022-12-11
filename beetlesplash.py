import os
import socket

show_author = False
show_quote = False

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(description="Prints a random quote and some information about the computer")
parser.add_argument("-v", "--version", help="show version information and exit", action="store_true")
parser.add_argument("--config", help="path to the config file")
args = parser.parse_args()
if args.version:
    print("beetlesplash 1.3")
    exit(0)
if args.config == None:
    print("\033[91mbeetlesplash error! No config file specified\033[0m")
    exit(1)
CONFIG_PATH = args.config

# Check if the terminal is big enough
if os.get_terminal_size().columns < 80 or os.get_terminal_size().lines < 24:
    print('\t\n\(")/\t\n-( )-\t\n/(_)\\\n\033[92mTerminal too small for beetles...\033[0m')
    exit(1)

# Check if the config file exists
if not os.path.isfile(CONFIG_PATH):
    print("\033[91mbeetlesplash error! Config file not found: " + CONFIG_PATH + "\033[0m")
    exit(1)

IMAGE_PATH = None
QUOTE_PATH = None
image_margin = 6
top_spacing_coefficient = 0.27
quote_width = 32
# Read the config file
with open(CONFIG_PATH, "r") as file:
    for line in file:
        line = line.rstrip()
        if line.startswith("quote_path = "):
            QUOTE_PATH = line[13:]
        elif line.startswith("show_author = "):
            show_author = line[14:] == "true"
        elif line.startswith("show_quote = "):
            show_quote = line[13:] == "true"
        elif line.startswith("image_path = "):
            IMAGE_PATH = line[13:]
        elif line.startswith("#") or line == "":
            continue
        elif line.startswith("image_margin = "):
            image_margin = int(line[15:])
        elif line.startswith("top_spacing_coefficient = "):
            top_spacing_coefficient = float(line[26:])
        elif line.startswith("quote_width = "):
            quote_width = int(line[14:])
        else:
            print("\033[91mbeetlesplash error! Unknown config option: " + line + "\033[0m")
            exit(1)

# Check if the image file exists
if not os.path.isfile(IMAGE_PATH):
    print("\033[91mbeetlesplash error! Image file not found: " + IMAGE_PATH + "\033[0m")
    exit(1)

# Class used to print colored text in the terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

data = []
image_width = 0
image_height = 0
terminal_width = os.get_terminal_size().columns
terminal_height = os.get_terminal_size().lines
# Read the file containing the ascii art
with open(IMAGE_PATH, "r") as file:
    for line in file:
        line = line.rstrip()
        image_width = max(image_width, len(line))
        data.append(line)
        image_height += 1

# Add spaces to the end of each line to make the image centered
for i in range(len(data)):
    data[i] += " " * (image_width - len(data[i])) + " " * image_margin

# Get information about the computer
info = []
# Get the username and hostname
username = os.getlogin()
hostname = socket.gethostname()
info.append(username + "@" + hostname)
# Get the ip address
ip = socket.gethostbyname(socket.gethostname())
info.append(ip)
# Get the current time
import datetime
now = datetime.datetime.now()
info.append(now.strftime("%d.%m.%Y %H:%M"))

image_width = image_width + image_margin

#  Load random quote from quotes.data
if show_quote:
    import random
    with open(QUOTE_PATH, "r") as file:
        quotes = file.readlines()
        quote = random.choice(quotes).split("~")

    # split the quote into lines
    quote_lines = []
    line = ""
    quote_width = min(quote_width, (terminal_width - image_width)//2-1)
    for word in quote[0].split():
        if len(line) + len(word) > quote_width:
            quote_lines.append(line)
            line = ""
        line += word + " "
    quote_lines.append(line)

    # Add the quote to the image
    for i in range(len(quote_lines)):
        info.append(bcolors.OKBLUE + quote_lines[i] + bcolors.ENDC)
    
    if show_author:
        author_line = bcolors.OKBLUE + "~ " + quote[1][:-1] + bcolors.ENDC
        info.append(" " * (image_margin + quote_width - len(author_line)) + author_line)

# Add the information to the image
for i in range(len(info)):
    data[i+3] += bcolors.OKGREEN + info[i] + bcolors.ENDC

top_spacing = int((terminal_height - image_height) * top_spacing_coefficient)
bottom_spacing = terminal_height - image_height - top_spacing - 3
print(top_spacing*"\n")

# Print the image
for line in data:
    print(" " * ((terminal_width - image_width)//2) + line)

print(bottom_spacing*"\n")
exit(0)
