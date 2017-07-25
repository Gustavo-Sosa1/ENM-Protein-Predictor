"""This module contains the overloaded RandomForestClassifier and method to help
us with feature engineering and model optimization

Includes:
    Class RandomForestClassifierWithCoef:
        Overloaded sklearn random forest classifier with feature importances as
        coef_

    Functions:
        1) optimize: makes it easy to optimize our hyperparameters
        2) recursive_feature_elimination: recursive feature elimination
        with 5 fold cross validation
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.grid_search import GridSearchCV

class RandomForestClassifierWithCoef(RandomForestClassifier):
    """Adds feature weights for each returned variable from the
    sklearn RandomForestClassifier:
    https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/ensemble/forest.py
    """
    def fit(self, *args, **kwargs):
        """Overloaded fit method to include the feature importances
        of each variable. This is used for RFECV
        """
        super(RandomForestClassifierWithCoef, self).fit(*args, **kwargs)
        self.coef_ = self.feature_importances_

def optimize(model, X_train, Y_train):
    """This function optimizes the machine learning classifier's hyperparameters,
    print the parameters that give the best accuracy based on a
    5 fold cross validation.

    Args:
        :param model (obj): The sklearn model you wish to optimize
        :param X_train (array): The X values of training data
        :param Y_train (array): The Y values of the training data

    Returns:
        None
    """
    #add whatever your heart desires to param grid, keep in mind its an incredibly inefficient algorithm
    param_grid = {
        'n_estimators': [1000],
        'max_features': ['auto'],
        'max_depth': [None],
        'min_samples_split': [5],
        'min_samples_leaf': [1],
        'n_jobs': [-1],
    }
    #5 fold validation
    CV_est = GridSearchCV(estimator=model, param_grid=param_grid, cv= 5)
    CV_est.fit(X_train, Y_train)
    print "Best parameters: \n {}".format(CV_est.best_params_)

def recursive_feature_elimination(model, X_train, Y_train):
    """Runs RFECV with 5 folds, prints optimum features
    useful for feature engineering

    Args:
        :param model (obj): The sklean model you wish to optimize
        :param X_train (array): The X values of training data
        :param Y_train (array): The Y values of the training data

    Returns:
        None
    """
    selector = RFECV(estimator=model, step=1, cv=5, scoring='roc_auc', verbose=1)
    selector = selector.fit(X_train, Y_train)
    print "selector support: \n {} \n selector ranking: \n {}".format(selector.support_, selector.ranking_)
    print "Optimal number of features: \n {} \n Selector grid scores: \n {} \n".format(selector.n_features_, selector.grid_scores_)
