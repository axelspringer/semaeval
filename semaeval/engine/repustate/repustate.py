"""
Repustate Python API client.

Requirements:
- Python 2.6+
- python-requests

Want to change it / improve it / share it? Go for it.

Feedback is appreciated at info@repustate.com

More documentation available at https://www.repustate.com/docs
"""
import urllib

import requests

class RepustateAPIError(Exception):
	pass

class Client(object):

	url_template = (
		'http://api.repustate.com/%(version)s/%(key)s/%(function)s.json'
	)

	def __init__(self, api_key, version='v3'):
		self.api_key = api_key
		self.version = version

	def _call_api(self, api_function, method='POST', **params):
		params = dict((x, y) for x, y in params.items() if y is not None)

		data = urllib.urlencode(params)

		url_args = dict(
			function=api_function,
			key=self.api_key,
			version=self.version,
			)

		url = self.url_template % url_args

		http_function = getattr(requests, method.lower())
		response = http_function(url, data=data)

		if response.status_code == 200:
			return response.json()
		elif response.status_code >= 500:
			raise RepustateAPIError('Internal Server Error: could not process your API call.')
		elif response.status_code >= 400:
			# Missing params, incorrect arguments supplied etc.
			msg = u'%(title)s\n\n%(description)s' % response.json()
			raise RepustateAPIError(msg)
		else:
			# Redirect maybe? Who knows, just return raw response.
			return response.content

	def sentiment(self, text, lang='en'):
		"""
		Retrieve the sentiment for a single URl or block of text.
		"""
		return self._call_api('score', text=text, lang=lang)

	def bulk_sentiment(self, items, lang='en'):
		"""
		Bulk score multiple pieces of text (not urls!). Each text gets an ID
		associated with it and the response will be a mapping of IDs ->
		sentiment scores.
		"""
		items_to_score = {}

		for idx, item in enumerate(items):
			items_to_score['text%d' % idx] = item

		return self._call_api('bulk-score', lang=lang, **items_to_score)

	def chunk(self, text, lang='en'):
		"""
		Chunk a block of text into smaller, logically grouped phrases. The
		sentiment of each chunk is also returned.
		"""
		return self._call_api('chunk', text=text, lang=lang)

	def categorize(self, text, niche, lang='en'):
		"""
		Chunk the `text` into categories as defined by `niche` and determine
		the sentiment for each chunk.
		"""
		return self._call_api('categorize', text=text, niche=niche, lang=lang)

	def add_catetory_rule(self, niche, category, query, weight, lang='en'):
		"""
		Add a rule (and category, niche) by which you want to classify text. If
		the niche and/or category previously didn't exist, they will be
		automatically created.

		The rule_id of the new rule will be returned.
		"""
		return self._call_api(
			'category-rules',
			niche=niche,
			category=category,
			query=query,
			weight=weight,
			lang=lang,
			)

	def delete_category_rule(self, rule_id):
		"""
		Delete a previously created custom rule. The `rule_id` was returned
		when add_category_rule was first called. Alternatively, you can call
		`list_category_rules` and retrieve the rule_id that way.
		"""
		return self._call_api('category-rules', method='DELETE', rule_id=rule_id)

	def list_category_rules(self):
		"""
		List all custom category rules you've created.
		"""
		return self._call_api('category-rules', method='GET')

	def add_sentiment_rule(self, text, sentiment, lang='en'):
		"""
		Create a custom sentiment rule. `text` can be a word or phrase that
		you'd like to define the sentiment for. `sentiment` should be one of:
		1. positive
		2. negative
		3. neutral
		"""
		return self._call_api('sentiment-rules', text=text, sentiment=sentiment, lang=lang)

	def delete_sentiment_rule(self, rule_id):
		return self._call_api('sentiment-rules', method='DELETE', rule_id=rule_id)

	def list_sentiment_rules(self):
		return self._call_api('sentiment-rules', method='GET')

	def commit_sentiment_rules(self):
		return self._call_api('sentiment-rules', method='PUT')

	def topic_sentiment(self, text, topics, lang='en'):
		"""
		Determine the sentiment of a block of text in the context of one or
		more topics. Multiple topics should be comma separated
		e.g. topic1,topic2,topic3
		"""
		return self._call_api('topic', text=text, topics=topics, lang=lang)

	def pos_tags(self, text, lang='en'):
		"""
		Get the part of speech tags for the given text. The full list of tags
		can be seen at https://www.repustate.com/docs/
		"""
		return self._call_api('pos', text=text, lang=lang)

	def entities(self, text, lang='en'):
		"""
		Extract any named entities from the text.
		"""
		return self._call_api('entities', text=text, lang=lang)

	def clean_html(self, url):
		"""
		Clean up a web page. It doesn't work well on home pages - it's designed
		for content pages.
		"""
		return self._call_api('clean-html', method='GET', url=url)

	def detect_language(self, text):
		"""
		Detect which language this text is in.
		"""
		return self._call_api('detect-language', text=text)
