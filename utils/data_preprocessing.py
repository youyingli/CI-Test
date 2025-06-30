import numpy as np

from rdkit import Chem
from rdkit.Chem import rdmolops, AllChem

# Ref : https://www.rdkit.org/docs/GettingStartedInPython.html
def smiles_to_graph(smiles: str, add_Hydrogen: bool = False) -> tuple[np.ndarray, np.ndarray]:
    mol = Chem.MolFromSmiles(smiles)

    if add_Hydrogen:
        mol=Chem.AddHs(mol)

    # Create 2D coordinate
    AllChem.Compute2DCoords(mol)

    # Catch conformer（2D）
    conf = mol.GetConformer()

    Atoms = []
    for atom in mol.GetAtoms():
        idx = atom.GetIdx()
        pos = conf.GetAtomPosition(idx)
        Atoms.append([atom.GetAtomicNum(), pos.x, pos.y])
        #atoms.append([atom.GetAtomicNum(), atom.GetSymbol(), pos.x, pos.y])
    Atoms = np.array(Atoms)

    # Build adjacency matrix using bonding type between moleculars
    """
     0: rdkit.Chem.rdchem.BondType.UNSPECIFIED
     1: rdkit.Chem.rdchem.BondType.SINGLE
     2: rdkit.Chem.rdchem.BondType.DOUBLE
     3: rdkit.Chem.rdchem.BondType.TRIPLE
     4: rdkit.Chem.rdchem.BondType.QUADRUPLE
     5: rdkit.Chem.rdchem.BondType.QUINTUPLE
     6: rdkit.Chem.rdchem.BondType.HEXTUPLE
     7: rdkit.Chem.rdchem.BondType.ONEANDAHALF
     8: rdkit.Chem.rdchem.BondType.TWOANDAHALF
     9: rdkit.Chem.rdchem.BondType.THREEANDAHALF
     10: rdkit.Chem.rdchem.BondType.FOURANDAHALF
     11: rdkit.Chem.rdchem.BondType.FIVEANDAHALF
     12: rdkit.Chem.rdchem.BondType.AROMATIC
     13: rdkit.Chem.rdchem.BondType.IONIC
     14: rdkit.Chem.rdchem.BondType.HYDROGEN
     15: rdkit.Chem.rdchem.BondType.THREECENTER
     16: rdkit.Chem.rdchem.BondType.DATIVEONE
     17: rdkit.Chem.rdchem.BondType.DATIVE
     18: rdkit.Chem.rdchem.BondType.DATIVEL
     19: rdkit.Chem.rdchem.BondType.DATIVER
     20: rdkit.Chem.rdchem.BondType.OTHER
     21: rdkit.Chem.rdchem.BondType.ZERO
    """

    Adjacency = Chem.rdmolops.GetAdjacencyMatrix(mol)
    for bond in mol.GetBonds():
        Adjacency[bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()] = float(bond.GetBondType())
        Adjacency[bond.GetEndAtomIdx(), bond.GetBeginAtomIdx()] = float(bond.GetBondType())

    return Atoms, Adjacency
