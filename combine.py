with open("merged.mp3", "wb") as outfile:
    for i in range(1, 14):
        with open(f"{i}.mp3", "rb") as infile:
            outfile.write(infile.read())
