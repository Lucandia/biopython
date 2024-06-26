# Copyright (C) 2012 by Eric Talevich.
# This code is part of the Biopython distribution and governed by its
# license. Please see the LICENSE file that should have been included
# as part of this package.

"""Unit tests for Bio.Phylo.Applications wrappers."""

import os
import unittest
import warnings

from Bio import Phylo
from Bio import MissingExternalDependencyError
from Bio import BiopythonDeprecationWarning


with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=BiopythonDeprecationWarning)
    from Bio.Phylo.Applications import RaxmlCommandline


raxml_exe = None
try:
    from subprocess import getoutput

    output = getoutput("raxmlHPC -v")
    if "not found" not in output and "not recognized" not in output:
        if "This is RAxML" in output:
            raxml_exe = "raxmlHPC"
except FileNotFoundError:
    pass

if not raxml_exe:
    raise MissingExternalDependencyError(
        "Install RAxML (binary raxmlHPC) if you want"
        " to test the Bio.Phylo.Applications wrapper."
    )

# Example Phylip file with 4 aligned protein sequences
EX_PHYLIP = "Phylip/interlaced2.phy"


class AppTests(unittest.TestCase):
    """Tests for application wrappers."""

    def test_raxml(self):
        """Run RAxML using the wrapper."""
        cmd = RaxmlCommandline(
            raxml_exe, sequences=EX_PHYLIP, model="PROTCATWAG", name="test"
        )
        # The parsimony seed should be set automatically
        self.assertIn("-p", str(cmd))
        # Smoke test
        try:
            out, err = cmd()
            self.assertGreater(len(out), 0)
            self.assertEqual(len(err), 0)
            # Check the output tree
            tree = Phylo.read("RAxML_result.test", "newick")
            self.assertEqual(tree.count_terminals(), 4)
        finally:
            # Remove RAxML-generated files, or RAxML will complain bitterly
            # during the next run
            for fname in [
                "RAxML_info.test",
                "RAxML_log.test",
                "RAxML_parsimonyTree.test",
                "RAxML_result.test",
                # Present in 7.2.X+  but not 7.0.4:
                "RAxML_bestTree.test",
            ]:
                if os.path.isfile(fname):
                    os.remove(fname)


# ---------------------------------------------------------

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
