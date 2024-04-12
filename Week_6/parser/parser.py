import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


# Read the standalone letter "C" here as "Complete"
NONTERMINALS = """
S -> Clause | Clause Conj Clause | Clause Conj VClause | Clause Conj VClause PPs

Clause -> NP VP | NP VClause | NP VClause PPs | NP VP PPs
VClause -> VP NP

NP -> N | Det N | Adj N | Adj Adj N | Adj Adj Adj N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N
PP -> P NP | P NP Adv
PPs -> PP | PP PP | PP PP PP
VP -> V | Adv V | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence: str) -> list[str]:
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence)
    result = []
    for word in words:
        if any(char.isalpha() for char in word):
            result.append(word.lower())

    return result


def np_chunk(tree: nltk.tree) -> list[nltk.tree]:
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    subtrees = [foo for foo in tree.subtrees() if foo.label() == "NP"]

    result = []
    for tree in subtrees:
        if any(sub != tree and sub.label() == "NP" for sub in tree.subtrees()):
            continue

        result.append(tree)

    return result


if __name__ == "__main__":
    main()
