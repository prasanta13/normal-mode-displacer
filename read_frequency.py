def read_freq(filename):
    # Initialize an empty list to store the frequencies
    freqcm1 = []

    # Open the file and read its contents
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Loop through the lines to find the frequencies
    for line in lines:
        if 'Frequencies ---' in line:
            # Split the line by whitespace and take the values after 'Frequencies ---'
            freq_values = line.split('Frequencies ---')[1].split()
            # Convert the string values to float and add to the list
            freqcm1.extend([float(freq) for freq in freq_values])

    # Print the list of frequencies
    #print(freqcm1)
    return freqcm1