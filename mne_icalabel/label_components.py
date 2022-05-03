from typing import Union

import numpy as np
from mne import BaseEpochs
from mne.io import BaseRaw
from mne.preprocessing import ICA
from mne.utils import _validate_type
from mne.utils.check import _check_option

from .iclabel import iclabel_label_components
from .iclabel.config import ICLABEL_NUMERICAL_TO_STRING
from .utils import _validate_inst_and_ica

methods = {
    "iclabel": iclabel_label_components,
}


def label_components(inst: Union[BaseRaw, BaseEpochs], ica: ICA, method: str):
    """Automatically label the ICA components with the selected method.

    Parameters
    ----------
    inst : Raw | Epochs
        The data instance used to fit the ICA instance.
    ica : ICA
        The fitted ICA instance.
    method : str
        The proposed method for labeling components. Must be one of:
        ``'iclabel'``.

    Returns
    -------
    component_dict : dict
        A dictionary with the following output:
        - 'y_pred_proba' : np.ndarray of shape (n_components, n_classes)
        Estimated corresponding predicted probabilities of output classes
        for each independent component.
        - 'y_pred' : list of shape (n_components,)
        The corresponding numerical label of the class with the highest
        predicted probability.
        - 'labels': list of shape (n_components,)
        The corresponding string label of each class in 'y_pred'.

    Notes
    -----
    For ICLabel model, the output classes are ordered:
    - 'Brain'
    - 'Muscle'
    - 'Eye'
    - 'Heart'
    - 'Line Noise'
    - 'Channel Noise'
    - 'Other'
    """
    _validate_type(method, str, "method")
    _check_option("method", method, methods)
    _validate_inst_and_ica(inst, ica)
    labels_pred_proba = methods[method](inst, ica)
    labels_pred = np.argmax(labels_pred_proba, axis=1)
    labels = [ICLABEL_NUMERICAL_TO_STRING[label] for label in labels_pred]

    component_dict = {
        "y_pred_proba": labels_pred_proba,
        "y_pred": labels_pred,
        "labels": labels,
    }
    return component_dict