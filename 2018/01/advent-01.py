frequency = 0
past_frequencies = set()
freq_match = False

past_frequencies.add(frequency)

while not freq_match:
    with open("input.txt") as openfile:
        for line in openfile:
            frequency += int(line)
            if frequency in past_frequencies:
                double_frequency = frequency
                freq_match = True
                break
            else:
                past_frequencies.add(frequency)

print(double_frequency)
