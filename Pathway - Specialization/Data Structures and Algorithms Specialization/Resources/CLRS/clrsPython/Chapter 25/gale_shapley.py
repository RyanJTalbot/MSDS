#!/usr/bin/env python3
# gale_shapley.py

# Introduction to Algorithms, Fourth edition
# Tom Cormen

#########################################################################
#                                                                       #
# Copyright 2022 Massachusetts Institute of Technology                  #
#                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining #
# a copy of this software and associated documentation files (the       #
# "Software"), to deal in the Software without restriction, including   #
# without limitation the rights to use, copy, modify, merge, publish,   #
# distribute, sublicense, and/or sell copies of the Software, and to    #
# permit persons to whom the Software is furnished to do so, subject to #
# the following conditions:                                             #
#                                                                       #
# The above copyright notice and this permission notice shall be        #
# included in all copies or substantial portions of the Software.       #
#                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                 #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS   #
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN     #
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE      #
# SOFTWARE.                                                             #
#                                                                       #
#########################################################################


def gale_shapley(men, women, mens_rankings, womens_rankings):
    """Gale-Shapley algorithm to solve the stable-marriage problem.

    Arguments:
        men -- list of men, by name
        women -- list of women, by name
        mens_rankings -- dictionary indexed by mens' names, with a list of women for each man
        womens_rankings -- dictionary indexed by women's names, with a list of men for each woman

    Returns:
        A list of pairs of men and women, together comprising a stable matching.
        """

    # Keep sets free_women and free_men of the currently free women and men.
    # Initially, all women and men are free.
    free_women = {*women}
    free_men = {*men}

    # Indices into womens_rankings of the next man to propose to.
    next_proposal = {}
    for w in women:
        next_proposal[w] = 0

    woman_engaged_to = {}  # dictionary of which woman each man is engaged to
    for m in men:
        woman_engaged_to[m] = None

    while len(free_women) > 0:  # while some woman is free
        # Select any free woman.
        w = free_women.pop()

        # Let m be the first man on w's ranked list to whom she has not proposed.
        m = womens_rankings[w][next_proposal[w]]
        next_proposal[w] += 1  # next time w proposes, it's to the next man in her ranking

        if m in free_men:  # is m free?
            # w and m become engaged to each other (and not free).
            woman_engaged_to[m] = w
            free_men.remove(m)
        else:  # does m prefer w to the woman w' he's currently engaged to?
            w_rank = mens_rankings[m].index(w)
            wprime = woman_engaged_to[m]
            wprime_rank = mens_rankings[m].index(wprime)
            if w_rank < wprime_rank:
                # m breaks the engagement to w', who becomes free
                free_women.add(wprime)
                # w and m become engaged to each other (and not free)
                woman_engaged_to[m] = w
            else:  # m rejects w, with w remaining free
                free_women.add(w)

    # Construct the list of engaged pairs.
    engaged_pairs = []
    for m in men:
        engaged_pairs.append((woman_engaged_to[m], m))

    return engaged_pairs


# Testing
if __name__ == "__main__":
    # Example from textbook with characters from "Corner Gas."
    women = ["Wanda", "Emma", "Lacey", "Karen"]
    men = ["Oscar", "Davis", "Brent", "Hank"]
    womens_rankings = {"Wanda": ["Brent", "Hank", "Oscar", "Davis"], "Emma": ["Davis", "Hank", "Oscar", "Brent"],
                       "Lacey": ["Brent", "Davis", "Hank", "Oscar"], "Karen": ["Brent", "Hank", "Davis", "Oscar"]}
    mens_rankings = {"Oscar": ["Wanda", "Karen", "Lacey", "Emma"], "Davis": ["Wanda", "Lacey", "Karen", "Emma"],
                     "Brent": ["Lacey", "Karen", "Wanda", "Emma"], "Hank": ["Lacey", "Wanda", "Emma", "Karen"]}
    matching = gale_shapley(men, women, mens_rankings, womens_rankings)
    print(matching)

    # Example from textbook with characters from "Friends."
    women = ["Monica", "Phoebe", "Rachel"]
    men = ["Chandler", "Joey", "Ross"]
    womens_rankings = {"Monica": ["Chandler", "Joey", "Ross"], "Phoebe": ["Joey", "Ross", "Chandler"],
                       "Rachel": ["Ross", "Chandler", "Joey"]}
    mens_rankings = {"Chandler": ["Phoebe", "Rachel", "Monica"], "Joey": ["Rachel", "Monica", "Phoebe"],
                     "Ross": ["Monica", "Phoebe", "Rachel"]}
    matching = gale_shapley(men, women, mens_rankings, womens_rankings)
    print(matching)
