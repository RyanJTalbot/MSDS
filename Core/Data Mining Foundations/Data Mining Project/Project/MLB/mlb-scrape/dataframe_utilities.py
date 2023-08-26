import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def fix_na(df, add_ind=True):
    '''
    my imputer. adds indicator column & replaces missing with median
    also fixes np.inf with 0
    '''
    # fix na
    missing_idx = df.isna().sum()[df.isna().sum() > 0].index
    for x in missing_idx:
        if add_ind:
            df[x + '_isna'] = df[x].isna()  # add idicator column

        if df[x].dtype == 'object':
            df[x].fillna('Unknown', inplace=True)
        else:
            df[x].fillna(df[x].median(), inplace=True)
    df.replace({np.inf: 0}, inplace=True)
    return df


def plot_confusion_matrix(y_true, y_pred, classes,
                          ax=None,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    if ax == None:
        fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    return ax
