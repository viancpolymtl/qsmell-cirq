""" Repeated set of operations on circuit (ROC) """

import sys
import pandas as pd
from .ISmell import *

class ROC(ISmell):

    def __init__(self):
        super().__init__("ROC")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        qubits = [bit for bit in df.index if bit.startswith('q-')]
        stamps = df.columns

        num_repetitions = 0
        for i in range(len(qubits)):
            qubit = qubits[i]
            row = df.loc[qubit]
            row = [op for op in row if op != '' and not op.lower().startswith('barrier')]

            # Lets assume row is composed by following string
            # UMEEB UMEEB UMEEB UMEEB

            j = 0
            while j < len(row):
                opx = row[j]
                print('j %d :: opx %s' %(j, opx)) # debug

                # For the running example, on the first iteraction,
                #   j is 0
                #   opx is U
                #
                # UMEEB UMEEB UMEEB UMEEB
                # ^
                # j
                #
                # For the running example, on the second iteraction,
                #   j is 5
                #   opx is U (once again)
                #
                # UMEEB UMEEB UMEEB UMEEB
                #       ^
                #       j

                # Try to find the next copy/repetition of opx
                stamp_next_opx = -1
                for k in range(j+1, len(row)):
                    opy = row[k]
                    print('  k %d :: opy %s' %(k, opy)) # debug

                    if opx == opy:
                        # Found the next copy/repetition of opx
                        stamp_next_opx = k
                        break
                        # For the running example, on the first iteraction of j,
                        #   j is 0
                        #   opx is U
                        #   stamp_next_opx is 5
                        #
                        # UMEEB UMEEB UMEEB UMEEB
                        # ^     ^
                        # j     |
                        #       |
                        #       stamp_next_opx
                if stamp_next_opx == -1:
                    # There is no next copy/repetition of opx
                    j += 1
                    continue
                print('  found a copy of opx %s in %d' %(opx, stamp_next_opx)) # debug

                # Is the sequence of operations on the next copy/repetition of opx
                # the same as in the original opx?
                rep_seq = None
                if stamp_next_opx - j == 1: # opy appears right after opx
                    rep_seq = True
                else:
                    for k in range(1, stamp_next_opx-j):
                        # For the running example, on the first iteraction of j,
                        #   j is 0
                        #   opx is U
                        #   stamp_next_opx is 5
                        #
                        # UMEEB UMEEB UMEEB UMEEB
                        # ^     ^
                        # j     |
                        #       |
                        #       stamp_next_opx
                        #
                        # First iteraction of k we have
                        #   k is 1
                        #   row[j+k] is M
                        #   row[stamp_next_opx+k] is M
                        #
                        #  row[j+k]
                        #  ˇ
                        # UMEEB UMEEB UMEEB UMEEB
                        #        ^
                        #        row[stamp_next_opx+k]
                        #
                        if stamp_next_opx+k == len(row):
                            # End of the row, no more ops to analyze
                            rep_seq = False
                            break
                        elif row[j+k] == row[stamp_next_opx+k]:
                            # Same op
                            rep_seq = True
                        else:
                            # Different op within the sequence
                            rep_seq = False
                            # No need to keep looking for
                            break
                assert rep_seq != None

                if rep_seq:
                    print('  and found a sequence %d::%d from %d' %(j, stamp_next_opx-1, stamp_next_opx))
                    j = stamp_next_opx
                    # For the running example, on the first iteraction of j,
                    #   j becomes stamp_next_opx => 5
                    #
                    # UMEEB UMEEB UMEEB UMEEB
                    #       ^
                    #       j
                    #
                    # Count it as a repetition
                    num_repetitions += 1
                else:
                    print('  but did not found a sequence %d::%d from %d' %(j, stamp_next_opx-1, stamp_next_opx))
                    j += 1
            break

        metrics = {
            'metric': self._name,
            'value': num_repetitions
        }

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')
