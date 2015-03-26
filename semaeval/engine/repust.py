# -*- coding: utf-8 -*-

import repustate

# see also here: https://www.repustate.com/media/entities.txt
label_repustate = {
"government.politician": "PERSON",
"location.citytown": "GEO",
"location.us_state": "GEO",
"location.country": "GEO",
"location.region": "GEO",
"location.continent": "GEO",
"location.nationality": "KEYWORD",
"business.businessmen": "PERSON",
"government.agency": "ORG",
"government.political_party": "ORG",
"government.us_presidents": "PERSON",
"government.position": "FUNCTION",
"business.job_title": "FUNCTION",
"business.brand": "PRODUCT",
"business.oil_and_gas_drilling_and_exploration":"ORG",
"business.apparel_stores":"PRODUCT",
"time.month": "DATE",
"time.day": "DATE",
"time.season": "DATE",
"news.network": "ORG",
"health.disease": "KEYWORD",
"health.vaccine": "KEYWORD",
"travel.hotel":"KEYWORD",
"travel.accommodation":"KEYWORD",
"health.physician": "PERSON",
"sports.sports_team_coach": "PERSON",
"sports.pro_athlete":"PERSON",
"finance.currency": "CURRENCY",
"automotive.model": "PRODUCT",
"automotive.company": "ORG",
"music.album": "PRODUCT"}


def convert_label(label):
	if label in label_repustate:
		return label_repustate[label]
	else:
		print "repustate:",label
		return label


def extract_entities(text, lang):
	entities = {}
	try:
		client = repustate.Client(api_key='317542394cddce0baf6b3ec698d92198e2b6e4a7')
		# see https://www.repustate.com/docs/
		response = client.entities(text=text.encode("utf-8"), lang=lang)

		for k,v in response['entities'].items():
			key = k
			value = v
			entities[key] = convert_label(value)
	except repustate.RepustateAPIError, e:
		print "Repustate API Error:", e, "No entities extracted!"

	return entities
