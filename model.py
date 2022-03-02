import dataset
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit


clf = LogisticRegression(random_state=0, max_iter=10000)


def prepare_dataset():
		

def train_model(df):
	df_model = df

	X = df_model.iloc[:,:-1].values
	y = df_model['DECEASED']
	groups = df_model['PATIENT']

	index = 0
	gss = GroupShuffleSplit(n_splits=1, train_size=.8, random_state=7)

	for train_idx, test_idx in gss.split(X, y, groups):
		X_train = X[train_idx]
		X_test = X[test_idx]
		y_train = y.iloc[train_idx]
		y_test = y.iloc[test_idx]
		clf.fit(X_train,y_train)

	return clf
		