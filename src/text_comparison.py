from difflib import SequenceMatcher

# We can add all the possible ways of comparing text here

#def compare_texts_similarity(text1, text2):
    #similarity = SequenceMatcher(None, text1, text2).ratio()
    #return similarity < 1.0  # Returns True if texts are different

def compare_texts_similarity(text1, text2):
    return text1 != text2 #Should return True


