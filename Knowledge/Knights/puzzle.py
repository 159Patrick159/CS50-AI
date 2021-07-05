from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave))
)
# Store A's statement
AS0 = And(AKnight,AKnave)

# If what A is saying is false then A is a knave
if not(model_check(knowledge0,AS0)):
    knowledge0.add(AKnave)
    knowledge0.add(Not(AS0))
# If what A is saying is true then A is a knight
elif model_check(knowledge0,AS0):
    knowledge0.add(AKnight)
    knowledge0.add(AS0)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Include rules of the game
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave))
)
# Store A statement in a variable
AS1 = And(AKnave,BKnave)
# If A is lying then A is a knave
if not model_check(knowledge1,AS1):
    knowledge1.add(AKnave)
    # Since A lied then its negation is the truth
    knowledge1.add(Not(AS1))
elif model_check(knowledge1,AS1):
    knowledge1.add(AKnight)
    # Since A told the truth we can add their statement to out KB
    knowledge1.add(AS1)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Set game rules
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnave,BKnight))
)
# Store A's and B's stament in a variable
AS2 = Or(And(AKnight,BKnight),And(AKnave,BKnave))
BS2 = Or(And(AKnight,BKnave),And(AKnave,BKnight))

# Follow same algorithm as before checking if their statements are true
if not model_check(knowledge2,AS2):
    # If their statements are lies then their negations are the truth
    knowledge2.add(Not(AS2))
    # If person lies then that person is a knave
    knowledge2.add(AKnave)
elif model_check(knowledge2,AS2):
    # Add their true statement to KB
    knowledge2.add(AS2)
    # Add them as knights
    knowledge2.add(AKnight)

# Same as before but with person B
if not model_check(knowledge2,BS2):
    knowledge2.add(Not(BS2))
    knowledge2.add(BKnave)
elif model_check(knowledge2,BS2):
    knowledge2.add(BS2)
    knowledge2.add(BKnight)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Set game rules
    Or(AKnave,AKnight),
    Or(BKnave,BKnight),
    Or(CKnave,CKnight),
    Not(And(AKnave,AKnight)),
    Not(And(BKnave,BKnight)),
    Not(And(CKnave,CKnight))
)
# Store each person's statement in a variable
AS3 = And(Or(AKnight,AKnave),Not(And(AKnight,AKnave)))
BS3 = AKnave
BS3_2 = CKnave
CS3 = AKnight
# Follo same algorithm as before but on all players
if not model_check(knowledge3,AS3):
    knowledge3.add(Not(AS3))
    knowledge3.add(AKnave)
elif model_check(knowledge3,AS3):
    knowledge3.add(AS3)
    knowledge3.add(AKnight)
# Check both statements of person B
if not model_check(knowledge3,BS3):
    knowledge3.add(Not(BS3))
    knowledge3.add(BKnave)
elif model_check(knowledge3,BS3):
    knowledge3.add(BS3)
    knowledge3.add(BKnight)

if not model_check(knowledge3,BS3_2):
    knowledge3.add(Not(BS3_2))
    knowledge3.add(BKnave)
elif model_check(knowledge3,BS3_2):
    knowledge3.add(BS3_2)
    knowledge3.add(BKnight)
# Check statement from person C 
if not model_check(knowledge3,CS3):
    knowledge3.add(Not(CS3))
    knowledge3.add(CKnave)
elif model_check(knowledge3,CS3):
    knowledge3.add(CS3)
    knowledge3.add(CKnight)

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
