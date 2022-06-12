# weighted-levenshtein-list
Calculate Levenshtein distance between tow strings or tow strings array, Optimal String Alignment distance and Damerau-Levenshtein distance, where the cost of each operation can be weighted by letter.

Use Cases
---------

Most existing Levenshtein libraries are not very flexible: all edit operations have cost 1.

However, sometimes not all edits are created equal. For instance, if you are doing OCR correction, maybe substituting '0' for 'O' should have a smaller cost than substituting 'X' for 'O'. If you are doing human typo correction, maybe substituting 'X' for 'Z' should have a smaller cost, since they are located next to each other on a QWERTY keyboard.

This library supports all theses use cases, by allowing the user to specify different weights for edit operations involving every possible combination of letters. The core algorithms are written in Cython, which means they are blazing fast to run.

The Levenshtein distance function supports setting different costs for inserting characters, deleting characters, and substituting characters. Thus, Levenshtein distance is well suited for detecting OCR errors.

The Damerau-Levenshtein distance function supports setting different costs for inserting characters, deleting characters, substituting characters, and transposing characters. Thus, Damerau-Levenshtein distance is well suited for detecting human typos, since humans are likely to make transposition errors, while OCR is not.

All function with parameter list like lev_list and lev_list_b ... are generator function. Generators are iterators, a kind of iterable you can only iterate over once. Generators do not store all the values in memory, they generate the values on the fly

More Information
----------------

Levenshtein distance:
https://en.wikipedia.org/wiki/Levenshtein\_distance and
https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer\_algorithm

Optimal String Alignment:
https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein\_distance#Optimal\_string\_alignment\_distance

Damerau-Levenshtein distance:
https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein\_distance#Distance\_with\_adjacent\_transpositions



Installation
------------

``pip install weighted_levenshtein_list``

Usage Example
-------------

.. code:: python

    import numpy as np
    from weighted_levenshtein_list import lev, osa, dam_lev ,lev_list_b, osa_list_b, dam_lev_list_b, lev_list,osa_list,dam_lev_list


    insert_costs = np.ones(2048, dtype=np.float64)  # make an array of all 1's of size 2048, the number of ASCII characters
    insert_costs[ord('D')] = 1.5  # make inserting the character 'D' have cost 1.5 (instead of 1)

    # you can just specify the insertion costs
    # delete_costs and substitute_costs default to 1 for all characters if unspecified
    print(lev('BANANAS', 'BANDANAS', insert_costs=insert_costs))  # prints '1.5'

    delete_costs = np.ones(2048, dtype=np.float64)
    delete_costs[ord('S')] = 0.5  # make deleting the character 'S' have cost 0.5 (instead of 1)

    # or you can specify both insertion and deletion costs (though in this case insertion costs don't matter)
    print(lev('BANANAS', 'BANANA', insert_costs=insert_costs, delete_costs=delete_costs))  # prints '0.5'


    substitute_costs = np.ones((2048, 2048), dtype=np.float64)  # make a 2D array of 1's
    substitute_costs[ord('H'), ord('B')] = 1.25  # make substituting 'H' for 'B' cost 1.25

    print(lev('HANANA', 'BANANA', substitute_costs=substitute_costs))  # prints '1.25'

    # it's not symmetrical! in this case, it is substituting 'B' for 'H'
    print(lev('BANANA', 'HANANA', substitute_costs=substitute_costs))  # prints '1'

    # to make it symmetrical, you need to set both costs in the 2D array
    substitute_costs[ord('B'), ord('H')] = 1.25  # make substituting 'B' for 'H' cost 1.25 as well

    print(lev('BANANA', 'HANANA', substitute_costs=substitute_costs))  # now it prints '1.25'

    #To Group values in a nested list with a one-liner Map / Zip without creating another list i will use list()

    print(list(lev_list(['HANANA','BANANA'],['BANANA','BONANA','ABNANO'], substitute_costs=substitute_costs)))
    # [('HANANA', [['BANANA', 1.25], ['BONANA', 2.25], ['ABNANO', 3.0]]), ('BANANA', [['BANANA', 0.0], ['BONANA', 1.0], ['ABNANO', 3.0]])]

    print(list(lev_list_b(['HANANA','BANANA'],['BANANA','BONANA','ABNANO'],3,0, substitute_costs=substitute_costs)))
    # print distance between 0 and 3 
    # [('HANANA', [['BANANA', 1.25], ['BONANA', 2.25]], 2), ('BANANA', [['BONANA', 1.0]], 1)]


    transpose_costs = np.ones((2048, 2048), dtype=np.float64)
    transpose_costs[ord('A'), ord('B')] = 0.75  # make swapping 'A' for 'B' cost 0.75

    # note: now using dam_lev. lev does not support swapping, but osa and dam_lev do.
    # See Wikipedia links for difference between osa and dam_lev
    print(dam_lev('ABNANA', 'BANANA', transpose_costs=transpose_costs))
    # prints '0.75'

    print(list(dam_lev_list(['ABNANA','BANANA'],['BANONA','BONANA','ABNANO'], transpose_costs=transpose_costs)))
    # [('ABNANA', [['BANONA', 1.75], ['BONANA', 2.0], ['ABNANO', 1.0]]), ('BANANA', [['BANONA', 1.0], ['BONANA', 1.0], ['ABNANO', 2.0]])]

    print(list(dam_lev_list_b(['ABNANA','BANANA'],['BANONA','BONANA','ABNANO'],3,1, transpose_costs=transpose_costs)))
    # print distance between 1 and 3 
    # [('ABNANA', [['BANONA', 1.75], ['BONANA', 2.0]], 2), ('BANANA', [['ABNANO', 2.0]], 1)]

    # like substitution, transposition is not symmetrical either!
    print(dam_lev('BANANA', 'ABNANA', transpose_costs=transpose_costs))  # prints '1'

    # you need to explicitly set the other direction as well
    transpose_costs[ord('B'), ord('A')] = 0.75  # make swapping 'B' for 'A' cost 0.75

    print(dam_lev('BANANA', 'ABNANA', transpose_costs=transpose_costs))  # now it prints '0.75'


``lev``, ``osa``, and ``dam_lev`` are aliases for ``levenshtein``,
``optimal_string_alignment``, and ``damerau_levenshtein``, respectively.


Source
---------

https://github.com/infoscout/weighted-levenshtein
