import numpy as np

# utils.data_preprocessing
from CI_Test.utils.data_preprocessing import *

def test_smiles_to_graph():

    _, Adjacency = smiles_to_graph('c1OOc1', add_Hydrogen=True)

    assert ( Adjacency == np.array([[ 0, 12,  0, 12,  1,  0],
                                    [12,  0, 12,  0,  0,  0],
                                    [ 0, 12,  0, 12,  0,  0],
                                    [12,  0, 12,  0,  0,  1],
                                    [ 1,  0,  0,  0,  0,  0],
                                    [ 0,  0,  0,  1,  0,  0]],  dtype=np.int32)).all()
