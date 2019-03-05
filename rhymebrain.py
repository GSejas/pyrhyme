__title__ = 'pyrhyme'
__version__ = '0.1'
__author__ = 'Jorge Sequeira'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019 Jorge Sequeira'


import warnings
import requests

from functools import partial


RHYMEBRAIN_API_ENDPOINT = 'http://rhymebrain.com'

DEFAULT_LANG = 'de'


class RhymeBrainApiException(Exception):
	pass


class AttrDict(dict):

	"""
	A subclass of dict that exposes keys as attributes
	"""

	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]

		try:
			return self[attr]
		except KeyError:
			raise AttributeError("'%s' object has no attribute '%s'" %
			                     (self.__class__.__name__, attr))

	def __setattr__(self, attr, value):
		if attr in self.__dict__:
			self.__dict__[attr] = value
		else:
			self[attr] = value


class RhymeWord(AttrDict):

	"""
    A special case AttrDict that handles data specifically being returned
    from the rhymebrain api (i.e. integer values converted from strings). The structure
    is very object-like, but retains all the qualities of a python dict.
    Attributes are not a direct mirror of rhymebrain api results, but follow this pattern::
        <Result Object>
            - id
            - word:  The rhyming word
            - score: 	The RhymeRankTM score for the word.
						Scores of 300 and above are perfect rhymes.
						Scores between 0 and 300 are near rhymes without similar sounding consonents.
						Words with the same score are listed with the most matching sounds first. If you later sort by score again, it is best to preserve this ordering before showing the results to the user.
            - flags: A list of letters giving more information about the word.
						a: The word is offensive.
						b: The word might be found in most dictionaries.
						c: The pronunciation is known with confidence. It was not automatically generated.
            - syllables: An estimate of the number of syllables in the rhyming word.
            - freq: 	A number that tells you how common the word is. The number is a logarithm of the frequency of usage in common texts. Currently, the highest possible value is 34.


			- pron: The result is a string containing the phonetic transcription of the word. 
					The arpabet format used is described here. The flags indicate whether the pronunciation is 
					automatically generated or not. An automatically generated pronunciation might not be accurate.
            - ipa: The phonetic transcription using the International Phonetic Alphabet.
					This transcription might contain unicode characters. Since the response is in JSON format, 
					the unicode characters are encoded using the \\u syntax.

			- combined: nOne or two possible spellings of the portmanteau. When there is more 
				than one possibility, they are separated by a comma.
            - source: The two words contained in the the portmanteau, separated by a comma.
    """

	def __init__(self, data=None):
		if data:
			super(RhymeWord, self).__init__(word=data.get('word'),
			                                score=data.get('score'),
			                    freq=data.get('freq'),
			                     flags=data.get('flags'),
			                     syllables=data.get('syllables'))

	def __repr__(self):
		return '%s<%s>' % (self.__class__.__name__, self.word)

	def __str__(self):
		return self.word

	__unicode__ = __str__


class RhymeBrain(object):

	"""
    A python wrapper around the RhymeBrain api. 
    """

	def __init__(self):
		pass 
	
	def _endpoint(self):
		return '/'.join((RHYMEBRAIN_API_ENDPOINT, 'talk'))
		

	def _check_or_raise(self, meta):
		if meta.get('status') != 200:
			raise RhymeBrainApiException(meta.get('error_message'))

	def _fetch(self, endpoint_name, **params):
		"""
		Wrapper for making an api request from rhymebrain
		"""
		params['function'] = endpoint_name
		print(params)
		resp = requests.get(self._endpoint(), params=params)
		print(resp.url)
		resp.raise_for_status()

		data = resp.json()
		# error = data.get('error')
		# self._check_or_raise(data.get('meta', {}))

		return data

	def rhyming(self, word=None, lang=DEFAULT_LANG, maxResults= None):
		"""
		Search for rhymes with a given word. 
		
		Note that this method is a RhymeWord generator. Optionally accepts a maximum number of results.
		:param word: Word to search a rhyme for
		:type term: string
		:param lang: ISO639-1 language code (optional). Eg. en, de, es, fr, ru
		:type phrase: string
		:param maxResults: (optional) The number of results to return. If you 
            do not include this parameter, RhymeBrain will choose how many words to 
            show based on how many good sounding rhymes there are for the word.
		:type limit: int
		"""
		assert (word)

		params = {'function':"",'word': word, 'lang': lang}

		# Optional parameter
		if maxResults:
			params.update({'maxResults': maxResults})

		fetch = partial(self._fetch, 'getRhymes', **params)

		data = fetch()

		for item in data:
			yield RhymeWord(item)

	def rhyming_list(self, word=None, lang=DEFAULT_LANG, maxResults= None):
		"""
		Suppose you expect the `rhyming` method to just give you a list rather
		than a generator. This method will have that effect. Equivalent to::
		    >>> g = RhymeBrain()
		    >>> results = list(g.rhyming('foo'))
        :param word: Word to search a rhyme for
        :type term: string
        :param lang: ISO639-1 language code (optional). Eg. en, de, es, fr, ru
        :type phrase: string
        :param maxResults: (optional) The number of results to return. If you 
            do not include this parameter, RhymeBrain will choose how many words to 
            show based on how many good sounding rhymes there are for the word.
        :type limit: int
		"""
		return list(self.rhyming(word=word, maxResults=maxResults, lang=lang))


def rhyming(word=None, lang=DEFAULT_LANG, maxResults= None):
	"""
	Shorthand for creating a RhymeBrain api wrapper
	and then calling the rhyming method. Note that this will return a generator
	"""
	return RhymeBrain().rhyming(
	        word=None, lang=DEFAULT_LANG, maxResults= None)


def rhyming_list(word=None, lang=DEFAULT_LANG, maxResults= None):
	"""
	Shorthand for creating a RhymeBrain api wrapper and then calling the rhyming_list method.
	"""
	return RhymeBrain().rhyming_list(
	        word=word, lang=lang, maxResults= maxResults)

