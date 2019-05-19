from answer_dict import answer_dicts

def recode_answers(dataset, q_num, lang, multi):
	"""
	Function to recode single choice questions from the questionaire

	dataset: the dataset containing the responses, pandas dataframe
	q_num: the question number to convert
	lang: which language is the questionaire in, possible values: 'en', 'fr' and 'de'
	multi: the type of question (whether single choice or multiple choice), boolean
	"""

	# determining which conversion dict to use
	dict_to_use = answer_dicts[lang][q_num]

	# reversing the dict
	dict_to_use = {v:k for k,v in dict_to_use.items()}

	# split answers if necessary
	if multi:
		# converting str to list
		col = [ans.split(';') if isinstance(ans, str) else ans for ans in dataset[q_num]]
		# recode
		recoded = [[dict_to_use[an] if an in dict_to_use.keys() else an for an in ans] if isinstance(ans, list) else ans for ans in col]
	else:
		col = dataset[q_num]
		# recode
		recoded = [dict_to_use[ans] if ans in dict_to_use.keys() else ans for ans in dataset[q_num]]

	return(recoded)