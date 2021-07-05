import csv
import itertools
import sys
from typing import Protocol

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_prob = 1
    for person in people:
        person_prob = 1
        # Check if person is in one_gene set
        if person in one_gene:
            # Check if person is a parent
            if people[person]["father"] == None and people[person]["mother"] == None:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["gene"][1]
            # Else the person is someone's child
            else:
                # Locate the person's parents
                father = people[person]["father"]
                mother = people[person]["mother"]

                # Father has 1 copy of gene
                if father in one_gene:
                    father_pass_on = 0.5
                # Father has 2 copies of gene
                elif father in two_genes:
                    father_pass_on = 1-(PROBS["mutation"])
                # Father has no copies of gene
                else:
                    father_pass_on = PROBS["mutation"]
                
                # Mother has 1 copy of gene
                if mother in one_gene:
                    mother_pass_on = 0.5
                # Mother has 2 copies of gene
                elif mother in two_genes:
                    mother_pass_on = 1 - (PROBS["mutation"])
                # Mother has no copies of gene
                else:
                    mother_pass_on = PROBS["mutation"]

                # Calculate the final probabilty of the person given 1 copy of gene
                person_prob *= (mother_pass_on * (1-father_pass_on)) + (father_pass_on * (1-mother_pass_on))
            # Multiply the person probability to the joint probability 
            joint_prob *= person_prob
            person_prob = 1

        # Check if person is in two_gene set
        if person in two_genes:
            # Check if person is a parent
            if people[person]["father"] == None and people[person]["mother"] == None:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["gene"][2]
            else:
                # Locate the person's parents
                father = people[person]["father"]
                mother = people[person]["mother"]

                # Father has 1 copy of gene
                if father in one_gene:
                    father_pass_on = 0.5
                # Father has 2 copies of gene
                elif father in two_genes:
                    father_pass_on = 1-(PROBS["mutation"])
                # Father has no copies of gene
                else:
                    father_pass_on = PROBS["mutation"]
                
                # Mother has 1 copy of gene
                if mother in one_gene:
                    mother_pass_on = 0.5
                # Mother has 2 copies of gene
                elif mother in two_genes:
                    mother_pass_on = 1 - (PROBS["mutation"])
                # Mother has no copies of gene
                else:
                    mother_pass_on = PROBS["mutation"]
                    
                # Calculate the final probabilty of the person given for 2 copies of gene
                person_prob *= mother_pass_on * father_pass_on 
            # Multiply the person probability to the joint probability 
            joint_prob *= person_prob
            person_prob = 1

        # Check if person is not in one_gene or two_gene set
        if person not in one_gene and person not in two_genes:
            # Check if person is a parent
            if people[person]["father"] == None and people[person]["mother"] == None:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["gene"][0]
            else:
                # Locate the person's parents
                father = people[person]["father"]
                mother = people[person]["mother"]

                # Father has 1 copy of gene
                if father in one_gene:
                    father_pass_on = 0.5
                # Father has 2 copies of gene
                elif father in two_genes:
                    father_pass_on = 1-(PROBS["mutation"])
                # Father has no copies of gene
                else:
                    father_pass_on = PROBS["mutation"]
                
                # Mother has 1 copy of gene
                if mother in one_gene:
                    mother_pass_on = 0.5
                # Mother has 2 copies of gene
                elif mother in two_genes:
                    mother_pass_on = 1 - (PROBS["mutation"])
                # Mother has no copies of gene
                else:
                    mother_pass_on = PROBS["mutation"]

                # Calculate the final probabilty of the person given 0 copies of gene
                person_prob *= (1-father_pass_on) * (1-mother_pass_on)
            # Multiply the person probability to the joint probability 
            joint_prob *= person_prob
            person_prob = 1

        # Check if person is in have_trait set
        if person in have_trait:
            if person in one_gene:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["trait"][1][True]
            elif person in two_genes:   
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["trait"][2][True]
            else:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["trait"][0][True]
            joint_prob *= person_prob
            person_prob = 1
        # Check if person not in have_trait set
        if person not in have_trait:
            if person in one_gene:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["trait"][1][False]
            elif person in two_genes:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["trait"][2][False]
            else:
                # We multiply by the unconditional probability given in PROBS
                person_prob *= PROBS["trait"][0][False]
            joint_prob *= person_prob
            person_prob = 1

    return(joint_prob)
    


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Check if person is in one_gene set
        if person in one_gene:
            # Update probability by adding p
            probabilities[person]["gene"].update({1:(probabilities[person]["gene"][1] + p)})
        # Check if person is in two_genes set
        if person in two_genes:
            # Update probability by adding p
            probabilities[person]["gene"].update({2:(probabilities[person]["gene"][2] + p)})
        # Check if person is in neither of both sets
        if person not in one_gene or person not in two_genes:
            probabilities[person]["gene"].update({0:(probabilities[person]["gene"][0] + p)}) 
        # Check if person is in have_trait set
        if person in have_trait:
            # Update probability by adding p
            probabilities[person]["trait"].update({True:(probabilities[person]["trait"][True] + p)})
        # Check if person is not in have_trait set
        if person not in have_trait:
            probabilities[person]["trait"].update({False:(probabilities[person]["trait"][False] + p)})

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Normalize the probability distribuition for number of genes
    for person in probabilities:
        a = probabilities[person]["gene"][0]
        b = probabilities[person]["gene"][1]
        c = probabilities[person]["gene"][2]
        # Check if any of these values is 0
        if a == 0 and b != 0 and c !=0:
            x = 0
            y = 1/(1+(c/b))
            z = 1/(1+(b/c))
        elif b == 0 and a != 0 and c != 0:
            x = 1/(1+(c/a))
            y = 0
            x = 1/(1+(a/c))
        elif c == 0 and a != 0 and b != 0:
            x = 1/(1+(b/a))
            y = 1/(1+(a/b))
            z = 0
        # Else none of the values are 0
        else:
            x =  1/(1+(b/a)+(c/a))
            y =  1/(1+(a/b)+(c/b))
            z =  1/(1+(a/c)+(b/c))
        # X, Y, Z are the nomalized values if the probability dist. for number of genes
        probabilities[person]["gene"].update({0:x})
        probabilities[person]["gene"].update({1:y})
        probabilities[person]["gene"].update({2:z})
    
    # Now we normalize the probability distribution for having the trait
    for person in probabilities:
        d = probabilities[person]["trait"][True]
        e = probabilities[person]["trait"][False]
        if d != 0 and e != 0:
            x = 1/(1+(e/d))
            y = 1/(1+(d/e))
        elif d == 0 and e != 0:
            x = 0
            y = 1
        elif d != 0 and e == 0:
            x = 1
            y = 0
        probabilities[person]["trait"].update({True:x})
        probabilities[person]["trait"].update({False:y})

if __name__ == "__main__":
    main()
