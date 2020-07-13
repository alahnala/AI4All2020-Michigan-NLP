import json
with open('Data/data-text-classification/recipes.json') as f:
    Recipes = json.load(f)
    
Ingredients = ['\n'.join(v['Ingredients']) for r,v in Recipes.items()]
Procedures = ['\n'.join(v['Procedure']) for r,v in Recipes.items()]







'''
Confusion Matrix Code
'''

import numpy as np
import matplotlib
matplotlib.rcParams.update({
	'font.family': 'serif',
})
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


def heatmap(data, row_labels, col_labels, vmin=None, ax=None,
			cbar_kw={}, cbarlabel="",xlabel=None, ylabel=None, **kwargs):
	"""
	Create a heatmap from a numpy array and two lists of labels.
	Parameters
	----------
	data
		A 2D numpy array of shape (N, M).
	row_labels
		A list or array of length N with the labels for the rows.
	col_labels
		A list or array of length M with the labels for the columns.
	ax
		A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
		not provided, use current axes or create a new one.  Optional.
	cbar_kw
		A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
	cbarlabel
		The label for the colorbar.  Optional.
	**kwargs
		All other arguments are forwarded to `imshow`.
	"""

	if not ax:
		ax = plt.gca()

	# Plot the heatmap
	im = ax.imshow(data, vmin=vmin, norm=Normalize(vmin=vmin), **kwargs)

	# Create colorbar
	cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
	cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

	# We want to show all ticks...
	ax.set_xticks(np.arange(data.shape[1]))
	ax.set_yticks(np.arange(data.shape[0]))
	# ... and label them with the respective list entries.
	ax.set_xticklabels(col_labels, fontdict={'fontsize':20})
	ax.set_yticklabels(row_labels, fontdict={'fontsize':20})

	# Let the horizontal axes labeling appear on top.
	ax.tick_params(top=False, bottom=True,
				   labeltop=False, labelbottom=True)

	# Rotate the tick labels and set their alignment.
# 	plt.setp(ax.get_xticklabels(), rotation=-90, ha="right", 
# 			  rotation_mode="anchor")

	plt.setp(ax.get_xticklabels(), rotation=60, ha="right")

	# Turn spines off and create white grid.
	for edge, spine in ax.spines.items():
		spine.set_visible(False)

	ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
	ax.set_xlabel(xlabel, fontsize=20)
	ax.set_ylabel(ylabel, fontsize=20)
	ax.set_title("{} and {}".format(xlabel, ylabel), pad=50, fontsize=20)
	# ax.set_xticks(np.arange(data.shape[1]+1), minor=True)
	ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
	ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
	ax.tick_params(which="minor", bottom=False, left=False)

	return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:0.0f}",
					 textcolors=["black", "white"],
					 threshold=None, **textkw):
	"""
	A function to annotate a heatmap.
	Parameters
	----------
	im
		The AxesImage to be labeled.
	data
		Data used to annotate.  If None, the image's data is used.  Optional.
	valfmt
		The format of the annotations inside the heatmap.  This should either
		use the string format method, e.g. "$ {x:.2f}", or be a
		`matplotlib.ticker.Formatter`.  Optional.
	textcolors
		A list or array of two color specifications.  The first is used for
		values below a threshold, the second for those above.  Optional.
	threshold
		Value in data units according to which the colors from textcolors are
		applied.  If None (the default) uses the middle of the colormap as
		separation.  Optional.
	**kwargs
		All other arguments are forwarded to each call to `text` used to create
		the text labels.
	"""

	if not isinstance(data, (list, np.ndarray)):
		data = im.get_array()

	# Normalize the threshold to the images color range.
	if threshold is not None:
		threshold = im.norm(threshold)
	else:
		threshold = im.norm(data.max())/2.

	# Set default alignment to center, but allow it to be
	# overwritten by textkw.
	kw = dict(horizontalalignment="center",
			  verticalalignment="center")
	kw.update(textkw)

	# Get the formatter in case a string is supplied
	if isinstance(valfmt, str):
		valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

	# Loop over the data and create a `Text` for each "pixel".
	# Change the text's color depending on the data.
	texts = []
	for i in range(data.shape[0]):
		for j in range(data.shape[1]):
			kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)], fontsize=20)
			text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
			texts.append(text)

	return texts


def make_heatmap(data_matrix, vocab_index=None, rows=None, cols=None, threshold=None, vmin=None, annotate=True, figsize=(20,15), xlabel=None, ylabel=None):
	plt.clf()

	fig, ax = plt.subplots(figsize=figsize)

	
	if not (rows and cols):

		im, cbar = heatmap(data_matrix.astype(float), list(vocab_index.keys()), list(vocab_index.keys()), ax=ax, cmap="Purples", xlabel=xlabel, ylabel=ylabel)
	else:
		im, cbar = heatmap(data_matrix.astype(float), list(rows.keys()), list(cols.keys()), vmin=vmin, ax=ax, cmap="Purples", xlabel=xlabel, ylabel=ylabel)

	if annotate:
		texts = annotate_heatmap(im, threshold=threshold)

	fig.tight_layout()
	plt.show()
    
# import pandas as pd
# import numpy as np
# from collections import Counter

# def actual_vs_predicted(actual, predicted):
    
#     classes = Counter(actual).keys()
#     co_occurrence_matrix =  np.zeros((len(languages), len(languages)))

#     for i, lang_1 in enumerate(languages):
#         for j, lang_2 in enumerate(languages):
#             co_occurrence_matrix[i][j] = len(data[lang_1][lang_2])

#     co_occurrence_matrix = np.matrix(co_occurrence_matrix)

#     lang_idx = {lang:i for i, lang in enumerate(languages)}

#     make_heatmap(co_occurrence_matrix, rows=lang_idx, cols=lang_idx, annotate=True, xlabel='Predicted', ylabel='Actual', figsize=(12,8))
    