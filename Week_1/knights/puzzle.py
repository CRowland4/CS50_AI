from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
ALie = Symbol("A told a lie")
ATruth = Symbol("A told the truth")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
BLie = Symbol("B told a lie")
BTruth = Symbol("B told the truth")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
CLie = Symbol("C told a lie")
CTruth = Symbol("C told the truth")

GameRules = And(
    # Nobody can tell both lie and tell the truth
    Not(And(ALie, ATruth)),
    Not(And(BLie, BTruth)),
    Not(And(CLie, CTruth)),

    # Nobody can be both a knight and a knave
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # You must either lie or tell the truth
    Or(ALie, ATruth),
    Or(BLie, BTruth),
    Or(CLie, CTruth),

    # Everyone is either a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    # If you lie, you're a knave, if you tell the truth, you're a knight
    Implication(ALie, AKnave),
    Implication(ATruth, AKnight),
    Implication(BLie, BKnave),
    Implication(BTruth, BKnight),
    Implication(CLie, CKnave),
    Implication(CTruth, CKnight),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    GameRules,
    Biconditional(And(AKnight, AKnave), ATruth)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    GameRules,
    Biconditional(And(AKnave, BKnave), ATruth)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    GameRules,
    Biconditional(And(AKnave, BKnave), ATruth),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A_says_knight = Symbol("A said 'I am a knight'")
A_says_knave = Symbol("A said 'I am a knave'")
knowledge3 = And(
    GameRules,
    Or(A_says_knave, A_says_knight),
    Implication(And(A_says_knight, AKnave), ALie),
    Implication(And(A_says_knight, AKnight), ATruth),
    Implication(And(A_says_knave, AKnave), ATruth),
    Implication(And(A_says_knave, AKnight), ALie),
    Biconditional(A_says_knave, BTruth),
    Biconditional(CKnave, BTruth),
    Biconditional(AKnight, CTruth),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
