## Load in 5 sequences of control cats (18 toes)
## and 5 sequences of case cats (22 toes)
import numpy as np
import scipy.stats as stats
import warnings
import Bio.PDB
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

warnings.filterwarnings("ignore")


def dna():
    cases = [
        'ACCTTGTAGTGTATTTTATGACCAAATGACTTTTTCCCCCCAGTGGCTAATTTGTCTCAGGCCTGCGTCTTAAAGAGACACGGTAATGAGTAGGAAGTCCAGCGTGGTCTGGA',
        'ACCTTGTACTGTATCTTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGTAATGAGTAGGAAGTCCAACGTGGTCTAGA',
        'GCCTTGTACTGTATATTATGACCAAATGACTTTTTCCACCCATTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGAAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGTAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGAAATGAGTAGGAAGTCCACCGTGGTCTAGA',
        'ACCTTGTAGTGTATTTTATGACCAAATGACTTTTTCCCCCCAGTGGCTAATTTGTCTCAGGCCTGCGTCTTAAAGAGACACGGTAATGAGTAGGAAGTCCAGCGTGGTCTGGA',
        'ACCTTGTACTGTATCTTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGTAATGAGTAGGAAGTCCAACGTGGTCTAGA',
        'GCCTTGTACTGTATATTATGACCAAATGACTTTTTCCACCCATTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGAAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGTAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACGGAAATGAGTAGGAAGTCCACCGTGGTCTAGA']
    controls = [
        'ACCTTGTACTGTATATTATGACCAAATGACTTTTTCCCCCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGAAATGAGTAGGAAGTCCACCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGTAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCATTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGTAATGAGTAGGAGGTCCAGCGTGGTCTAGA',
        'GCCTTGTACTGTATTTTATGACCAAATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTGCGTCTTAAAGAGACACAGTAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATCTTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGAAATGAGTAGGAAGTCCAACGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAAATGACTTTTTCCCCCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGAAATGAGTAGGAAGTCCACCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGTAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATATTATGACCAGATGACTTTTTCCACCCATTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGTAATGAGTAGGAGGTCCAGCGTGGTCTAGA',
        'GCCTTGTACTGTATTTTATGACCAAATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTGCGTCTTAAAGAGACACAGTAATGAGTAGGAAGTCCAGCGTGGTCTAGA',
        'ACCTTGTACTGTATCTTATGACCAGATGACTTTTTCCACCCAGTGGCTAATTTGTCTCAGGCCTCCGTCTTAAAGAGACACAGAAATGAGTAGGAAGTCCAACGTGGTCTAGA']
    length = len(cases[1])


    ## Find the frequency of each nucleotide in each position, to find the positions
    ## where the sequences are different.

    def freq_lists(dna_list):
        n = len(dna_list[0])
        A = [0] * n
        T = [0] * n
        G = [0] * n
        C = [0] * n
        for dna in dna_list:
            for index, base in enumerate(dna):
                if base == 'A':
                    A[index] += 1
                elif base == 'C':
                    C[index] += 1
                elif base == 'G':
                    G[index] += 1
                elif base == 'T':
                    T[index] += 1
        return A, C, G, T


    freqcases = np.array(freq_lists(cases)) / 5
    freqcontrols = np.array(freq_lists(controls)) / 5

    ## Compare the nucleotide frequencies in the normal cats, and the many-toed cats
    result = []
    for nuc in range(4):  # For each possible marker nucleotide, run a statistical test for each position
        test = []
        for i in range(length):
            n, p = stats.chisquare([freqcases[nuc, i], freqcontrols[nuc, i]])
            test.append([n, p])
        test = np.array(test)
        result.append([np.nanargmin(test[:, 1]), np.nanmin(test[:, 1])])

    ## Output the statistical test results
    print("Position, P-value")
    print("A nucleotide:", result[0])
    print("C nucleotide:", result[1])
    print("G nucleotide:", result[2])
    print("T nucleotide:", result[3])


def hemoglobin():
    # Import the Hemoglobin coordinates file from the Protein Data Bank.
    structure = Bio.PDB.PDBParser(QUIET=True).get_structure('Hemoglobin', 'data/1a3n.pdb')

    # Define a function to build a model of the protein from the coordinates
    def build_model(structure):
        angles = []
        for model in structure:
            for chain in model:
                polypeptides = Bio.PDB.CaPPBuilder().build_peptides(chain)
                for poly_index, poly in enumerate(polypeptides):
                    phi_psi = poly.get_phi_psi_list()
                    for res_index, residue in enumerate(poly):
                        phi, psi = phi_psi[res_index]
                        if phi and psi:
                            angles.append(['Hemoglobin', str(chain.id), residue.resname,
                                           residue.id[1], phi / np.pi, psi / np.pi])
        return np.array(angles)

    # Run our function.
    angles = build_model(structure)
    phi = np.array(angles[:, 4], dtype='float')
    psi = np.array(angles[:, 5], dtype='float')

    # Plot the results
    f, ax = plt.subplots(1)

    ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
    ax.xaxis.set_major_locator(tck.MultipleLocator(base=0.5))
    ax.yaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
    ax.yaxis.set_major_locator(tck.MultipleLocator(base=1))
    plt.ylim((-1, 1))
    plt.xlim((-1, 1))
    plt.xlabel('$\phi$')
    plt.ylabel('$\psi$')
    ax.scatter(phi, psi)

    plt.savefig("Islands.png", format="png")


hemoglobin()