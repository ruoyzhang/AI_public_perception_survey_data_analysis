import pandas as pd

def group_columns(dataset):
	"""
	a function to group together columns
	returns a dictionary
	keys refer to the question number 
	values refer to the actual column names
	"""

	# locating the columns to be reorganised
	cols = dataset.columns[6:(len(dataset.columns)-1)]

	# setting vars to represent the questions for easy ref
	questions = {}
	for question in cols:
		key = question.split(".")[0]
		if key not in questions.keys():
			questions[key] = [question]
		else:
			questions[key].append(question)

	return(questions)




def consolidate_mc(dataset, questions, q_number):
	"""
	a function to consolidate the multiple columns involved in a single multiple choice question

	dataset: the pandas Dataframe object
	questions: the 'questions' dict returned by the function 'group_columns'
	q_number:  int or str, the question number to deal with
	"""
	q_number = str(int(q_number))
	q_answers = []
	for _, row in dataset[questions[q_number]].iterrows():
		answers = [elem for elem in row if not pd.isnull(elem)]
		answers = [answer.split('.')[0] for answer in answers]
		q_answers.append(answers)

	return(q_answers)


def simplify_sgq(dataset, q_number):
	"""
	function to simply single choice questions
	we get rid of the text and only keep the ref(ind)

	dataset: the dataset, a pandas Dataframe object
	q_number: int or str, the question number to deal with
	"""
	# reformating the q_number variable
	q_number = int(q_number)
	q_number = "q{:02}".format(q_number)

	# converting
	answers = [answer.split('.')[0] for answer in dataset[q_number]]

	return(answers)