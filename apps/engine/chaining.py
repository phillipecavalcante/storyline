

def implies(hyp):

    searcher = get_searcher_doc(hyp)
    
    text = searcher.search(hyp)[0]
    
    return text


def storyline(hyp):

    max_docs = 10
    count = 0
    chaining = []
    
    while count < max_docs or not (hyp in chaining):
        chaining.append(hyp)
        count = count + 1
        text = implies(hyp)
        hyp = text
    
    return chaining
