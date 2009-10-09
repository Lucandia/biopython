# Copyright (C) 2009 by Eric Talevich (eric.talevich@gmail.com)
# This code is part of the Biopython distribution and governed by its
# license. Please see the LICENSE file that should have been included
# as part of this package.

"""Classes corresponding to Newick trees.

See classes in Bio.Nexus: Trees.Tree, Trees.NodeData, and Nodes.Chain.
"""
__docformat__ = "epytext en"

import warnings

import BaseTree


def deprecated(hint):
    """Decorator for deprecated Nexus functions.

    'hint' is the recommended replacement function or method.
    """
    message = "use %s instead" % hint
    def wrapper(func):
        warnings.warn(message, DeprecationWarning, stacklevel=3)
        return func
    return wrapper


# XXX from Bio.Nexus.Trees
# move to Utils?
def consensus(trees, threshold=0.5,outgroup=None):
    """Compute a majority rule consensus tree of all clades with relative
    frequency>=threshold from a list of trees.
    """


class NHTree(BaseTree.Tree):
    """Newick Tree object.
    """
    def __init__(self, root=None, clades=None, rooted=False, id=None, name='',
            weight=1.0,
            # values_are_support=False, max_support=1.0
            ):
        BaseTree.Tree.__init__(self,
                root=root or NHNode(), # originally the NodeData class
                clades=clades,            # list of NHNodes
                rooted=rooted,
                id=id,
                name=name)
        self.weight = weight
        # self.__values_are_support = values_are_support
        # self.max_support = max_support

    # Ported from Bio.Nexus.Trees.Tree

    # Methods with deprecated arguments -- duplicated in Bio.Tree.BaseTree

    def is_terminal(self, node=None):
        """Returns True if all direct descendents are terminal."""
        # Deprecated Newick behavior
        if node is not None:
            warnings.warn("use node.is_terminal() method instead",
                          DeprecationWarning, stacklevel=2)
            return node.is_terminal()
        return (not self.clades)

    def is_preterminal(self, node=None):
        """Returns True if all direct descendents are terminal."""
        # Deprecated Newick behavior
        if node is not None:
            warnings.warn("use node.tree.is_preterminal() method instead",
                          DeprecationWarning, stacklevel=2)
            return node.tree.is_preterminal()
        if self.is_terminal():
            return False
        for clade in self.clades:
            if not clade.is_terminal():
                return False
        return True
        # Py2.5+ one-liner:
        # return (not self.is_terminal()) and all(t.is_terminal() for t in self)

    # Deprecated methods from Bio.Nexus.Trees.Tree

    @deprecated("count_leaves")
    def count_terminals(self, node=None):
        if node is not None:
            warnings.warn("use node.tree.count_leaves() directly",
                          DeprecationWarning, stacklevel=2)
            return node.tree.count_leaves()
        return self.count_leaves()

    @deprecated("get_leaves")
    def get_terminals(self):
        """Return an iterable of all terminal nodes."""
        return self.get_leaves()

    @deprecated("\"not node.is_terminal()\"")
    def is_internal(self, node):
        """Returns True if node is an internal node."""
        return not node.is_terminal()

    @deprecated("root.tree.branch_length_to(node)")
    def sum_branchlength(self, root, node):
        """Adds up the branchlengths from root (default self.root) to node."""
        return root.tree.branch_length_to(node)

    @deprecated("node.tree.findall(Node)")
    def get_taxa(self, node_id=None):
        """Return a list of all OTUs downwards from a node (self, node_id)."""
        if node_id is None:
            node_id = self
        return list(node_id.tree.findall(BaseTree.Node))

    @deprecated("node.tree.findall(name=taxon).next()")
    def search_taxon(self, taxon):
        """Returns the first matching taxon in self.data.taxon.

        Not restricted to terminal nodes.

        node_id = search_taxon(self,taxon)
        """
        return self.findall(name=taxon).next()

    # TODO - port the rest of these methods to NHTree or BaseTree
    # See unit tests

    # XXX from Nexus.Nodes.Chain

    def is_parent_of(self, parent, grandchild):
        """Check if grandchild is a subnode of parent."""
        # XXX direct descendent? or "parent.get_path(grandchild) is not None"?

    # XXX from Nexus.Trees.Tree
    # """Get information about trees (monphyly of taxon sets, congruence between
    # trees, common ancestors,...) and to manipulate trees (reroot trees, split
    # terminal nodes)."""

    def collapse_genera(self,space_equals_underscore=True):
        """Collapses all subtrees which belong to the same genus.

        (i.e share the same first word in their taxon name.
        """
        # XXX whoa! this sounds error-prone


    def split(self, parent_id=None, n=2, branchlength=1.0):
        """Speciation: generates n (default two) descendants of a node.

        [new ids] = split(self,parent_id=None,n=2,branchlength=1.0):
        """ 

    def prune(self, taxon):
        """Prunes a terminal taxon from the tree.

        If taxon is from a bifurcation, the connectiong node will be collapsed
        and its branchlength added to remaining terminal node. This might be no
        longer a meaningful value'

        @return previous node
        """

    def set_subtree(self, node):
        """Return subtree as a set of nested sets."""

    def is_identical(self,tree2):
        """Compare tree and tree2 for identity."""
        return self.set_subtree(self.root)==tree2.set_subtree(tree2.root)

    def is_compatible(self, tree2, threshold, strict=True):
        """Compares branches with support>threshold for compatibility."""

    def is_monophyletic(self, taxon_list):
        """Return node_id of common ancestor if taxon_list is monophyletic, -1 otherwise."""

    def is_bifurcating(self, node=None):
        """Return True if tree downstream of node is strictly bifurcating."""

    def branchlength2support(self):
        """Move values stored in data.branchlength to data.support, and set
        branchlength to 0.0

        This is necessary when support has been stored as branchlength (e.g.
        paup), and has thus been read in as branchlength. 
        """

    def convert_absolute_support(self, nrep):
        """Convert absolute support (clade-count) to rel. frequencies.

        Some software (e.g. PHYLIP consense) just calculate how often clades
        appear, instead of calculating relative frequencies.
        """

    def has_support(self, node=None):
        """Returns True if any of the nodes has data.support != None."""

    def randomize(self, ntax=None, taxon_list=None, branchlength=1.0, branchlength_sd=None, bifurcate=True):
        """Generates a random tree with ntax taxa and/or taxa from taxlabels.

        Trees are bifurcating by default. (Polytomies not yet supported).

        @return new tree
        """

    def display(self):
        """Quick and dirty lists of all nodes."""

    def unroot(self):
        """Define a unrooted Tree structure, using data of a rooted Tree."""

    def root_with_outgroup(self, outgroup=None):
        """???

        Hint:
            Hook subtree starting with node child to parent.
        """

    def merge_with_support(self, bstrees=None, constree=None, threshold=0.5, outgroup=None):
        """Merge clade support with phylogeny.

        From consensus or list of bootstrap-trees.

        tree=merge_bootstrap(phylo,bs_tree=<list_of_trees>)
        or
        tree=merge_bootstrap(phylo,consree=consensus_tree with clade support)
        """


class NHNode(BaseTree.Node):
    """Newick Node object.
    """
    def __init__(self, tree=None, label=None, branch_length=1.0,
            support=None, comment=None):
        BaseTree.Node.__init__(self,
                tree=tree or NHTree(), # a.k.a. taxon; self.tree.root == self
                label=label,
                branch_length=branch_length)
        self.support = support
        self.comment = comment

    # Deprecated attributes from Bio.Nexus.Trees

    @property
    @deprecated('Node.label')
    def id(self):
        return self.label

    @property
    @deprecated("the Node object's attributes")
    def data(self):
        return _NodeData(taxon=self.tree,
                        branchlength=self.branch_length,
                        support=self.support,
                        comment=self.comment)

class _NodeData:
    """Stores tree-relevant data associated with nodes (e.g. branches or OTUs).

    This exists only for backward compatibility with Bio.Nexus, and is
    deprecated.
    """
    def __init__(self, taxon, branchlength, support, comment):
        self.taxon = taxon
        self.branchlength = branchlength
        self.support = support
        self.comment = comment

