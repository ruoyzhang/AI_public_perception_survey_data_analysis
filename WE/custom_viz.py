import pandas as pd
import pickle
from matplotlib import pyplot as plt
import os
from collections import Counter
from WE.answer_dict import uk_dict

class custom_viz():
	"""
	a custom class for fast visualisation of our survey data based on predetermined rules for the type of questions

	We divide the questions primarily into 2 big categories:
		Perception questions : q01 - q24
		Demographic questions : q25 - q29
	When we visualise the Perception questions, we provide the option to add extra dimensions from the demographic variables
	Moreover, the questions can be divided into 3 types based on viz style:
		Single choice - pie chart
		Multiple choice - Bar chart
		Likert scale - likert scale viz
	"""

	def __init__(self, dataset_cn, dataset_we):
		"""
		init method

		data_set_cn: the CN dataset, a dataframe object
		data_set_we: the WE dataset, a dataframe object
		"""

		# storing them as class variables for easy reference
		self.data_cn = dataset_cn
		self.data_we = dataset_we

	