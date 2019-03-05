pyrhyme
========

``pyrhyme`` is a wrapper around the RhymeBrain_ api. It aims to provide a pythonic way for interacting with the RhymeBrain_ api.


Requirements, Installing, and Compatibility
-------------------------------------------

The only requirement, included in ``requirements.txt`` is for requests_. If you
are using pip, you can install ``pyrhyme``:

.. code-block:: bash

    $ pip install requests pyrhyme

Alternatively:

.. code-block:: bash

    $ pip install requests
    $ pip install -e git+https://github.com/GSejas/pyrhyme.git#egg=pyrhyme

Then you should be off and running. ``pyrhyme`` has been tested against python
version 3.6.


Getting Started
---------------

Using ``pyrhyme`` is straightforward and aims provide interaction with
the api without any JSON interaction.

The entry point for interacting with Giphy_ api is the ``pyrhyme.RhymeBrain``
class. This class optionally accepts two arguments: ``api_key`` and ``strict``.
The ``api_key`` agument, when not preset, will default to the public key
(see above). The ``strict`` argument controls how you expect the api to
react when no results are returned. If enabled, an exception is raised,
otherwise, ``None`` is returned.


.. code-block:: python

    >>> import pyrhyme
    >>> g = pyrhyme.RhymeBrain()

Now you're ready to get started. There are a few key methods of the
``pyrhyme.RhymeBrain`` object that you'll want to know about

rhymimg
++++++
Search for rhymes with a given word. 
        
Note that this method is a RhymeWord generator. Optionally accepts a maximum number of results.

- **word**: Word to search a rhyme for
- **lang**: ISO639-1 language code (optional). Eg. en, de, es, fr, ru
- **maxResults**: (optional) The number of results to return. If you do not include this parameter, RhymeBrain will choose how many words toshow based on how many good sounding rhymes there are for the word.


rhyme_list
+++++++++++
Suppose you expect the `rhyming` method to just give you a list rather
than a generator. This method will have that effect. Equivalent to:

.. code-block:: python

    >>> g = pyrhyme.RhymeBrain()
    >>> results = [x for x in g.rhymimg('foo')]



------------------------------------------------------------------------------

.. note::
    The above methods of ``pyrhyme.RhymeBrain`` are also exposed at the module
    level for your convenience. For example:

    .. code-block:: python

        >>> from pyrhyme import rhyming
        >>> img = rhyming('foo', lang='en')

------------------------------------------------------------------------------


Handling Results
----------------

All results that represent a single image are wrapped in a
``pyrhyme.RhymeWord`` object. This object acts like a dictionary, but
also exposes keys as attributes. Note, that these are **not** a direct
mirror of api response objects; their goal is to be simpler. Structure
follows this layout::

    <Result Object>
        - word:  The rhyming word
        - score:    The RhymeRankTM score for the word.
                    Scores of 300 and above are perfect rhymes.
                    Scores between 0 and 300 are near rhymes without similar sounding consonents.
                    Words with the same score are listed with the most matching sounds first. If you later sort by score again, it is best to preserve this ordering before showing the results to the user.
        - flags: A list of letters giving more information about the word.
                    a: The word is offensive.
                    b: The word might be found in most dictionaries.
                    c: The pronunciation is known with confidence. It was not automatically generated.
        - syllables: An estimate of the number of syllables in the rhyming word.
        - freq:     A number that tells you how common the word is. The number is a logarithm of the frequency of usage in common texts. Currently, the highest possible value is 34.


        - pron: The result is a string containing the phonetic transcription of the word. 
                The arpabet format used is described here. The flags indicate whether the pronunciation is 
                automatically generated or not. An automatically generated pronunciation might not be accurate.
        - ipa: The phonetic transcription using the International Phonetic Alphabet.
                This transcription might contain unicode characters. Since the response is in JSON format, 
                the unicode characters are encoded using the \\u syntax.

        - combined: nOne or two possible spellings of the portmanteau. When there is more 
            than one possibility, they are separated by a comma.
        - source: The two words contained in the the portmanteau, separated by a comma.

For example:

.. code-block:: python

    >>> from pyrhyme import rhyme
    >>> r = rhyme('foo')
    >>> r.word


Changelog
---------

0.1
+++

- Initial Version


Contribution and License
------------------------

Developed by `Jorge Sequeira`_ and is licensed under the terms of a MIT license.
Contributions are welcomed and appreciated!


.. _RhymeBrain: https://rhymebrain.com
.. _requests: https://pypi.python.org/pypi/requests/1.2.3
.. _`api docs`: https://rhymebrain.com/api.html
.. _`Jorge Sequeira`: jsequeira03@gmail.com
