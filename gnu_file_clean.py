import sys
import re
import math

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Open the unedited file
input = open(input_filename,"r")
# Open a new file
output = open(output_filename,"a")

# Read in each line of the file into a list
lines = input.readlines()

# Re write the first two lines as is
output.write(lines[0])
output.write(lines[1])

# Declare
raw_residues = []
residues = []
hbonds = {}

# Split the 3rd line of the file by comma
raw_residues = lines[2].split(',')

# Take the raw residues and clean them up - don't remove duplicates
for entry in raw_residues:
    split_entry = entry.split(' ')
    for mol in split_entry:
        if re.search('MOL', mol):
            residue_name = re.search('-(.+?)@', mol).group(1)
            residue_name = re.sub('_', '', residue_name)
            
    residues.append(residue_name)

# Remove duplicates
clean_residues = list(dict.fromkeys(residues))
formatted_residues = ""
it = 1

# Generate a new line 3
for residue in clean_residues:
    if it == 1:
        formatted_residues = formatted_residues + "set ytics(\"" + residue + "\""
    else:
        formatted_residues = formatted_residues + "\"" + residue + "\""

    if it < 10:
        formatted_residues = formatted_residues + "    " + str(it) + ".000"
    elif 10 <= it < 100:
        formatted_residues = formatted_residues + "   " + str(it) + ".000"
    elif it >= 100:
        formatted_residues = formatted_residues + "  " + str(it) + ".000"

    it = it + 1

    if it <= len(clean_residues):
        formatted_residues = formatted_residues + ","

formatted_residues = formatted_residues + ")"

# Write new line 3
output.write(formatted_residues+"\n")

# Write lines 4 & 5
output.write(lines[3])
output.write(lines[4])

# fix the yrange (line 6)
yrange = "set yrange [   0.000:"

if len(clean_residues)+2 < 10:
    yrange = yrange + "   " + str(len(clean_residues)+2) + ".000"
elif 10 <= len(clean_residues)+2 < 100:
    yrange = yrange + "  " + str(len(clean_residues)+2) + ".000"
elif len(clean_residues)+2 >= 100:
    yrange = yrange + " " + str(len(clean_residues)+2) + ".000"

yrange = yrange + "]"

output.write(yrange+"\n")

# Write lines 7 & 8
output.write(lines[6])
output.write(lines[7])

# Read through each frame (start at line 9) - identify hbond residues - store the information for later
it = 8

# While the line at iterator doesn't say "end"
while not re.search('end', lines[it]):
    hbond_residues = []

    # For each line in the file starting from the line #iterator
    for line in lines[it:]:
        # remove leading and trailing whitespace
        line = line.strip()

        # if the first digit of the line is a number
        if line[:1].isdigit():
            # split the line (removing whitespace) and store the three parts in an array
            current_entry = line.split()

            frame = math.trunc(float(current_entry[0]))
            residue_number = math.trunc(float(current_entry[1]))

            # if there is an hbond and this isn't a duplicate residue save it in an array
            if current_entry[2] == '1' and not residues[residue_number-1] in hbond_residues:
                    hbond_residues.append(residues[residue_number])

            it = it + 1
        else:
            # if the line doesn't start with a number stop iterating
            it = it + 1
            break
    
    #  build the new line of the file
    for index, residue in enumerate(clean_residues):
        index = index + 1
        formatted_entry = ""

        # current entry [0] holds the frame number
        formatted_entry = formatted_entry + "   " + current_entry[0]

        if index < 10:
            formatted_entry = formatted_entry + "    " + str(index) + ".000"
        elif 10 <= index < 100:
            formatted_entry = formatted_entry + "   " + str(index) + ".000"
        elif index >= 100:
            formatted_entry = formatted_entry + "  " + str(index) + ".000" 

        if residue in hbond_residues:
            formatted_entry = formatted_entry + "             " + "1"
        else:
            formatted_entry = formatted_entry + "             " + "0"

        output.write(formatted_entry+"\n")
    
    terminator = "   " + current_entry[0]

    if len(clean_residues)+1 < 10:
        terminator = terminator + "    " + str(len(clean_residues)+1) + ".000 0"
    elif 10 <= len(clean_residues)+1 < 100:
        terminator = terminator + "   " + str(len(clean_residues)+1) + ".000 0"
    elif len(clean_residues)+1 >= 100:
        terminator = terminator + "  " + str(len(clean_residues)+1) + ".000 0"

    output.write(terminator+"\n\n")

# write the footer
output.write("end\npause -1\n")

input.close()
output.close()