import rhymebrain

rb = rhymebrain.RhymeBrain()
for obt in rb.rhyming_list(word="Dorf"):
    print(obt["word"])
    print(obt.freq)