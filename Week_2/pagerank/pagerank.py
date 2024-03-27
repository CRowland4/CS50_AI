import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus: dict[str, set], page: str, damping_factor: float) -> dict[str, float]:
    """
    <corpus> maps a page name to a set of all pages linked to by that page
    <page> represents the page the random surfer is currently on
    <damping_factor> is the damping factor to be used in calculating the probabilities

    Return a probability distribution over which page to visit next,
    given a current page.

    With probability <damping_factor>, choose a link at random
    linked to by <page>. With probability `1 - <damping_factor>`, choose
    a link at random chosen from all pages in the corpus.
    """
    if not corpus[page]:
        equal_probability = 1 / len(corpus)
        return {link: equal_probability for link in corpus}

    P_each_link_from_page_links = damping_factor / len(corpus[page])
    P_each_link_from_corpus = (1 - damping_factor) / len(corpus)

    result = dict()
    for link in corpus:
        if link in corpus[page]:
            result[link] = P_each_link_from_corpus + P_each_link_from_page_links
        else:
            result[link] = P_each_link_from_corpus
    return result


def sample_pagerank(corpus: dict[str, set], damping_factor: float, n: int) -> dict[str, float]:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {link: 0 for link in corpus}
    new_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        transition = transition_model(corpus, new_page, damping_factor)
        choices = list(transition.keys())
        weights = list(transition.values())

        new_page = random.choices(population=choices, weights=weights, k=1)[0]
        counts[new_page] += 1

    return {page: counts[page] / n for page in counts}


def iterate_pagerank(corpus: dict[str, set], damping_factor: float) -> dict[str, float]:
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_total_pages = len(corpus)
    result = {page: 1 / num_total_pages for page in corpus}

    while True:
        new_result = {}
        for page_p in corpus:
            sum_prob_p_chosen_from_i = 0
            for page_i in corpus:
                if not corpus[page_i]:
                    sum_prob_p_chosen_from_i += result[page_i] / num_total_pages
                elif page_p in corpus[page_i]:
                    sum_prob_p_chosen_from_i += result[page_i] / len(corpus[page_i])

            new_page_rank = ((1 - damping_factor) / num_total_pages) + (damping_factor * sum_prob_p_chosen_from_i)
            new_result[page_p] = new_page_rank

        if all(abs(result[page] - new_result[page]) < .001 for page in corpus):
            return new_result
        else:
            result = new_result


if __name__ == "__main__":
    main()
