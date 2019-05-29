import pandas as pd
import pickle
import numpy as np
import os
from collections import Counter
from WE.answer_dict import uk_dict
import plotly.graph_objs as go
from options import q_options, f_options

class custom_viz():
	"""
	a custom class for fast prepping survey data based on predetermined rules for the type of questions

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
		# please do NOT modify these class variables under any circumstance
		self.data_cn = dataset_cn
		self.data_we = dataset_we
		self.names = ['China', 'Western Europe']
		self.q_num_2_title = {v:k for k,v in q_options.items()}
		self.q02_correct = [0,1,1,0,0,0,1,0,0,1]

	def distribute(self, q_type_num):
		"""
		method used to decide which type of data preparation to execute

		q_num: the question number
		"""
		# process q_num
		q_type, q_num = q_type_num.split(',')

		# determinig which class method to use
		if q_type == 'sc':
			return(self.prep_data_SC(q_num))
		elif q_type == 'mc':
			return(self.prep_data_MC(q_num))
		elif q_type == 'sco':
			return(self.prep_score(q_num))
		elif q_type == 'ls':
			return(self.prep_data_likert(q_num))

	def prep_data_SC(self, q_num):
		"""
		method used to prep data for single choice questions

		q_num: which question to visualise
		"""

		# place holder for appending data and annotations
		data_combined = []
		annotations = []

		# annocation locations x-axis
		x_loc = [0.2, 0.8]

		for i, dset in enumerate([self.data_cn, self.data_we]):
			# counting responses
			count_data = {k:v for k,v in Counter(dset[q_num]).items() if k in uk_dict[q_num].keys()}

			# obtaining the letter label
			labels = sorted(count_data.keys())
			# converting to the text label
			labels_full = [uk_dict[q_num][label] for label in labels]

			# getting the count values
			values = [count_data[label] for label in labels]

			# plotly input format
			plotly_formatted_data = {
				'values': values,
				'labels': labels_full,
				'domain': {'column': i},
				'name': self.names[i],
				'hoverinfo': 'label+percent+name',
				'hole': 0.5,
				'type': 'pie'
			}

			# append data
			data_combined.append(plotly_formatted_data)

			# plotly layout annotations
			plotly_annotation = {'shadow': False,
				'text': self.names[i],
				'x': x_loc[i],
				'y': 1,
				'ax': 0,
				'ay': 0
				}

			# append annotations
			annotations.append(plotly_annotation)

		# specifying layout
		layout = {
			'title': self.q_num_2_title[q_num],
			'grid': {'rows': 1, 'columns': 2},
			'annotations': annotations
		}

		# combine data and layout
		to_return = {'data':data_combined, 'layout': layout}
		
		return(to_return)

	def prep_data_MC(self, q_num):
		"""
		method used to prep data for multiple choice questions
		this method will produce a vertical bar chart, no other options will be given

		q_num: which question to visualise
		"""

		# placeholder
		data_combined = []

		for i, dset in enumerate([self.data_cn, self.data_we]):

			# getting rid of NaN and other unwanted entries
			responses = [ans for ans in dset[q_num] if isinstance(ans, list)]

			# flattening lists
			flattened = [item.strip() for sublist in responses for item in sublist]

			# getting rid of 'other:___' answers
			flattened = [ans for ans in flattened if ans in uk_dict[q_num].keys()]

			# counting responses
			count_data = Counter(flattened)

			# obtaining the letter label
			labels = sorted(uk_dict[q_num].keys())

			# converting to the text label
			labels_full = [uk_dict[q_num][label] for label in labels]

			# getting normalised count values (%)
			values = [count_data[label]/sum(count_data.values()) if label in count_data.keys() else 0 for label in labels]

			# plotly input format
			plotly_formatted_data = {
				'y': values,
				'x': labels_full,
				'name': self.names[i],
				'hoverinfo': 'label+percent+name',
				'type': 'bar'
			}

			# append
			data_combined.append(plotly_formatted_data)

		# specifying layout
		layout = {
			'title': self.q_num_2_title[q_num],
			'xaxis': dict(tickangle=-90),
			'barmode': 'group'
		}

		# combine data and layout
		to_return = {'data':data_combined, 'layout': layout}
		
		return(to_return)

	def prep_score(self, q_num):
		"""
		method used to prep data for question 02 ONLY
		this method will produce a vertical bar chart, no other options will be given

		q_num: which question to visualise
		"""

		# placeholder
		data_combined = []

		# processing data
		for i,dset in enumerate([self.data_cn, self.data_we]):

			# calculating the similarity
			scores = [np.dot(self.q02_correct, ans) for ans in dset[q_num]]

			# counting discret scores
			score_counts = Counter(scores)

			# setting the labels
			labels = list(range(1,5))

			# normalise
			values = [100*score_counts[key]/sum(score_counts.values()) if key in score_counts.keys() else 0 for key in labels]


			# plotly input format
			plotly_formatted_data = {
				'y': values,
				'x': labels,
				'name': self.names[i],
				'hoverinfo': 'label+y+name',
				'type': 'bar'
			}

			# append
			data_combined.append(plotly_formatted_data)

		# specifying layout
		layout = {
			'title': self.q_num_2_title[q_num],
			'xaxis': dict(tickangle=0),
			'barmode': 'group'
		}

		# combine data and layout
		to_return = {'data':data_combined, 'layout': layout}

		return(to_return)

	def prep_data_likert(self, q_num):
		"""
		method used to prep data for questions of the likert scale nature
		this method will produce a likert viz based on horizontal bar charts

		q_num: which question to visualise
		"""

		# determining if we have the 10-y comparison
		if '_' in q_num:
			# split q_num into 2
			q_nums = q_num.split('_')
		else:
			# put it into a list
			q_nums = [q_num]

		# placeholder
		data_combined = []

		# get labels
		labels = list(range(1,8))

		# set colours
		likert_colors = ["#BD2F28", "#D14030", "#FA8E8E", "gainsboro", "#5BCAFF", "#2D7EFF", "#2B59FF"]

		# processing data
		# count for rating for TODAY and in 10 years
		count_today_cn = Counter(self.data_cn[q_nums[0]])
		count_today_we = Counter(self.data_we[q_nums[0]])

		# normalise
		values_today_cn = [round(100*count_today_cn[key]/sum(count_today_cn.values()), 2) if key in count_today_cn.keys() else 0 for key in labels]
		values_today_we = [round(100*count_today_we[key]/sum(count_today_we.values()), 2) if key in count_today_we.keys() else 0 for key in labels]

		# if we have the 10-y comparison, we execute the same calculations with the 10-y data
		if len(q_nums) > 1:
			count_10y_we = Counter(self.data_we[q_nums[1]])
			count_10y_cn = Counter(self.data_cn[q_nums[1]])
			values_10y_cn = [round(100*count_10y_cn[key]/sum(count_10y_cn.values()), 2) if key in count_10y_cn.keys() else 0 for key in labels]
			values_10y_we = [round(100*count_10y_we[key]/sum(count_10y_we.values()), 2) if key in count_10y_we.keys() else 0 for key in labels]
			# zip data so that we can stack properly
			zipped = list(zip(values_10y_we, values_today_we, values_10y_cn, values_today_cn))
		# if not we only zip the necessary lists
		else:
			zipped = list(zip(values_today_we, values_today_cn))

		# format data into required form
		for j, pair in enumerate(zipped):
			plotly_formatted_data = {
				'x': pair,
				#'domain': {'column': i},
				'name': labels[j],
				'hoverinfo': 'x+name',
				'type': 'bar',
				'orientation': 'h',
				'marker': {'color': likert_colors[j]}
			}
			# if we have 10-y comparison
			if len(q_nums) > 1:
				y = {'y': ['WE: in 10 Yrs', 'WE: today', 'CN: in 10 Yrs', 'CN: today']}
			else:
				y = {'y': ['WE', 'CN']}

			# combine
			plotly_formatted_data = {**plotly_formatted_data, **y}
				
			# append
			data_combined.append(plotly_formatted_data)

		# layout
		layout = {
			'title': self.q_num_2_title[q_num],
			#'grid': {'rows': 1, 'columns': 2},
			'barmode': 'stack'
		}

		# combine data and layout
		to_return = {'data': data_combined, 'layout': layout}

		return(to_return)