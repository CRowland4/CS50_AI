import csv
import itertools
import sys

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
    # if len(sys.argv) != 2:  # TODO uncomment
    #     sys.exit("Usage: python heredity.py data.csv")
    # people = load_data(sys.argv[1])

    people = load_data("data/family1.csv")  # TODO comment out
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
                print(p)
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


def joint_probability(people: dict[str, dict], one_gene: set[str], two_genes: set[str], have_trait: set[str]):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        1. everyone in set `one_gene` has one copy of the gene, and
        2. everyone in set `two_genes` has two copies of the gene, and
        3. everyone not in `one_gene` or `two_gene` does not have the gene, and
        4. everyone in set `have_trait` has the trait, and
        5. everyone not in set` have_trait` does not have the trait.
    """
    prob_1 = probability_one_gene_people(people, one_gene, two_genes)
    prob_2 = probability_two_gene_people(people, one_gene, two_genes)
    prob_3 = probability_zero_gene_people(people, one_gene, two_genes)
    prob_4 = probability_has_trait_people(one_gene, two_genes, have_trait)
    prob_5 = probability_not_has_trait_people(one_gene, two_genes, set(people.keys()).difference(have_trait))


    # First joint probability distribution for family1.csv: 1.3470359924494777e-09
    #  Should have gotten between: [0.007987000000000001, 0.008187]

    joint_prob = prob_5 * prob_4 * prob_3 * prob_2 * prob_1
    return joint_prob


def probability_not_has_trait_people(one_gene: set[str], two_gene: set[str], does_not_have_trait: set[str]) -> float:
    result = 1
    for person in does_not_have_trait:
        if person in one_gene:
            result = result * PROBS["trait"][1][False]  # Works
        elif person in two_gene:
            result = result * PROBS["trait"][2][False]
        else:
            result = result * PROBS["trait"][0][False]  # Works

    return result


def probability_has_trait_people(one_gene: set[str], two_gene: set[str], have_trait: set[str]) -> float:
    result = 1
    for person in have_trait:
        if person in one_gene:
            result = result * PROBS["trait"][1][True]
        elif person in two_gene:
            result = result * PROBS["trait"][2][True]  # Works
        else:
            result = result * PROBS["trait"][0][True]

    return result


def probability_zero_gene_people(people: dict[str, dict], one_gene: set[str], two_genes: set[str]) -> float:
    zero_genes = {person for person in people if person not in one_gene.union(two_genes)}

    result = 1
    for person in zero_genes:
        if not people[person]["mother"] and not people[person]["father"]:
            result = result * PROBS["gene"][0]  # Works
        else:
            mother_gene_count = get_parent_gene_count(people[person]["mother"], one_gene, two_genes)
            father_gene_count = get_parent_gene_count(people[person]["father"], one_gene, two_genes)
            result = result * probability_child_has_zero_gene(mother_gene_count, father_gene_count)

    return result


def probability_two_gene_people(people: dict[str, dict], one_gene: set[str], two_genes: set[str]) -> float:
    result = 1
    for person in two_genes:
        if not people[person]["mother"] and not people[person]["father"]:
            result = result * PROBS["gene"][2]  # Works
        else:
            mother_gene_count = get_parent_gene_count(people[person]["mother"], one_gene, two_genes)
            father_gene_count = get_parent_gene_count(people[person]["father"], one_gene, two_genes)
            result = result * probability_child_has_two_gene(mother_gene_count, father_gene_count)

    return result


def probability_one_gene_people(people: dict[str, dict], one_gene: set[str], two_genes: set[str]) -> float:
    result = 1
    for person in one_gene:
        if not people[person]["mother"] and not people[person]["father"]:
            result = result * PROBS["gene"][1]
        else:
            mother_gene_count = get_parent_gene_count(people[person]["mother"], one_gene, two_genes)  # Works
            father_gene_count = get_parent_gene_count(people[person]["father"], one_gene, two_genes)  # Works
            result = result * probability_child_has_one_gene(mother_gene_count, father_gene_count)

    return result


def probability_child_has_zero_gene(parent_gene_count1: int, parent_gene_count2: int) -> float:
    has_from_parent1 = probability_child_has_gene_from_parent(parent_gene_count1)
    has_from_parent2 = probability_child_has_gene_from_parent(parent_gene_count2)

    return (1 - has_from_parent1) * (1 - has_from_parent2)


def probability_child_has_two_gene(parent_gene_count1: int, parent_gene_count2: int) -> float:
    has_from_parent1 = probability_child_has_gene_from_parent(parent_gene_count1)
    has_from_parent2 = probability_child_has_gene_from_parent(parent_gene_count2)

    return has_from_parent1 * has_from_parent2


def probability_child_has_one_gene(parent_gene_count1: int, parent_gene_count2: int) -> float:
    has_from_parent1 = probability_child_has_gene_from_parent(parent_gene_count1)
    has_from_parent2 = probability_child_has_gene_from_parent(parent_gene_count2)

    return (has_from_parent1 * (1 - has_from_parent2)) + (has_from_parent2 * (1 - has_from_parent1))  # Works


def probability_child_has_gene_from_parent(parent_gene_count: int) -> float:
    if parent_gene_count == 0:
        return PROBS["mutation"]  # Works
    if parent_gene_count == 1:
        return .5

    return 1 - PROBS["mutation"]  # Works


def get_parent_gene_count(person: str, one_gene: set[str], two_genes: set[str]) -> int:
    if person in one_gene:
        return 1
    if person in two_genes:
        return 2

    return 0


def update(probabilities: dict[str, dict], one_gene: set, two_genes: set, have_trait: set, p: float) -> None:
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in one_gene:
        probabilities[person]["gene"][1] += p
    for person in two_genes:
        probabilities[person]["gene"][2] += p
    for person in set(probabilities.keys()).difference(one_gene.union(two_genes)):
        probabilities[person]["gene"][0] += p
    for person in have_trait:
        probabilities[person]["trait"][True] += p
    for person in set(probabilities.keys()).difference(have_trait):
        probabilities[person]["trait"][False] += p

    return


def normalize(probabilities: dict[str, dict]) -> None:
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        probabilities[person] = normalize_distribution(probabilities[person], "gene")
        probabilities[person] = normalize_distribution(probabilities[person], "trait")

    return


def normalize_distribution(person: dict[str, dict], distribution: str) -> dict[str, dict]:
    alpha = 1 / sum(list(person[distribution].values()))
    for key in person[distribution].keys():
        person[distribution][key] = person[distribution][key] * alpha

    return person


if __name__ == "__main__":
    main()
