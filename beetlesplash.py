import os
import socket

show_author = True
show_quote = True

# Parse command line arguments
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-h":
        print("Usage: python3 splash.py [OPTION]")
        print("Prints a random quote and some information about the computer")
        print("Options:")
        print("  -h  show this help message and exit")
        print("  -v  show version information and exit")
        print("--quote show a random quote")
        print("--author show the author of the quote")
        exit(0)
    elif sys.argv[1] == "-v":
        print("beetlesplash 1.2")
        exit(0)
    elif sys.argv[1] == "--no-quote":
        show_quote = False
    elif sys.argv[1] == "--no-author":
        show_author = False
    else:
        print("Unknown option: " + sys.argv[1])
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
with open("/home/tototmek/Projects/Python/beetlesplash/beetle_processed.txt", "r") as file:
    for line in file:
        line = line.rstrip()
        image_width = max(image_width, len(line))
        data.append(line)
        image_height += 1
image_margin = 7

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
    with open("/home/tototmek/Projects/Python/beetlesplash/quotes.data", "r") as file:
        quotes = file.readlines()
        quote = random.choice(quotes).split("~")

    # split the quote into lines
    quote_width = 32
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

top_spacing_coefficient = 0.33
top_spacing = int((terminal_height - image_height) * top_spacing_coefficient)
bottom_spacing = terminal_height - image_height - top_spacing - 3
print(top_spacing*"\n")

# Print the image
for line in data:
    print(" " * ((terminal_width - image_width)//2) + line)

print(bottom_spacing*"\n")
exit(0)