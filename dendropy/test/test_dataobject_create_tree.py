#! /usr/bin/env python

###############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2009 Jeet Sukumaran and Mark T. Holder.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

"""
Tests creation, reading, update, deletion of TreeList objects.
"""

import unittest
from cStringIO import StringIO
from dendropy.utility import error
from dendropy.test.support import framework
from dendropy.test.support import datagen
import dendropy

class TreeListCreateTest(framework.DataObjectVerificationTestCase):

    def setUp(self):
        self.tree_list1 = datagen.reference_tree_list()
        self.tree_list1_stream = StringIO(self.tree_list1.as_string("newick"))

    def testDeepCopyTreeListFromTreeListSameTaxa(self):
        tree_list2 = dendropy.TreeList(self.tree_list1, taxon_set=self.tree_list1.taxon_set)
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=False, equal_oids=False, distinct_trees=True)

    def testDeepCopyTreeListFromTreeListSameTaxa(self):
        tree_list2 = dendropy.TreeList([dendropy.Tree(t) for t in self.tree_list1], taxon_set=self.tree_list1.taxon_set)
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=False, equal_oids=False, distinct_trees=True)

    def testShallowCopyTreeListFromListSameTaxa(self):
        src_trees = [t for t in self.tree_list1]
        tree_list2 = dendropy.TreeList(src_trees, taxon_set=self.tree_list1.taxon_set)
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=False, equal_oids=False, distinct_trees=False)

    def testDeepCopyTreeListFromTreeListDifferentTaxa(self):
        tree_list2 = dendropy.TreeList(self.tree_list1)
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=True, equal_oids=False, distinct_trees=True)

    def testDeepCopyTreeListFromTreeListDifferentTaxa(self):
        tree_list2 = dendropy.TreeList([dendropy.Tree(t) for t in self.tree_list1])
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=True, equal_oids=False, distinct_trees=True)

    def testTooManyPosArgs(self):
        self.assertRaises(error.TooManyArgumentsError, dendropy.TreeList, self.tree_list1, dendropy.TreeList())

    def testMultipleSources(self):
        self.assertRaises(error.MultipleInitializationSourceError, dendropy.TreeList, self.tree_list1, stream=self.tree_list1_stream, format="newick")

    def testTreeListFromTreeFileSameTaxa(self):
        tree_list2 = dendropy.TreeList(stream=self.tree_list1_stream, format="newick", taxon_set=self.tree_list1.taxon_set)
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=False, equal_oids=False, distinct_trees=True)

    def testTreeListFromTreeFileDifferentTaxa(self):
        tree_list2 = dendropy.TreeList([dendropy.Tree(t) for t in self.tree_list1])
        self.assertDistinctButEqual(self.tree_list1, tree_list2, distinct_taxa=False, equal_oids=False, distinct_trees=True)

    def testTreeListFromTreeFileNoFormatSpecification(self):
        self.assertRaises(error.UnspecifiedFormatError, dendropy.TreeList, stream=self.tree_list1_stream)

    def testTreeListFromTreeFileNoKeywords(self):
        self.assertRaises(error.InvalidArgumentTypeError, dendropy.TreeList, stream=self.tree_list1_stream, format="newick")

#    def testTreeFromTreeSetOidAndLabelSameTaxa(self):
#        tree2 = dendropy.Tree(self.tree1, oid="TREE2", label="TREE2")
#        self.assertEqual(tree2.oid, "TREE2")
#        self.assertEqual(tree2.label, "TREE2")
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=False, equal_oids=False)
#
#    def testTreeFromTreeWithExtraKeywordArgs(self):
#        self.assertRaises(TypeError, dendropy.Tree, self.tree1, format="newick")
#
#    def testTreeFromTreeWithExtraPosArgs(self):
#        self.assertRaises(TypeError, dendropy.Tree, self.tree1, "dummy")
#
#    def testTreeFromInvalidObjectPosArgs(self):
#        self.assertRaises(TypeError, dendropy.Tree, object())
#
#    def testTreeFromInvalidIterablePosArgs(self):
#        self.assertRaises(TypeError, dendropy.Tree, "abcde")
#
#    def testTreeFromInvalidObjectPosArgsWithKeywords(self):
#        self.assertRaises(TypeError, dendropy.Tree, "xx", stream=StringIO(self.tree1_newick_str), format="newick")
#
#    def testTreeFromFileKeywordArgsDistinctTaxa(self):
#        tree2 = dendropy.Tree(stream=StringIO(self.tree1_newick_str), format="newick")
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=True, equal_oids=False)
#
#    def testTreeFromFileKeywordArgsSameTaxa(self):
#        tree2 = dendropy.Tree(stream=StringIO(self.tree1_newick_str), format="newick", taxon_set=self.tree1.taxon_set)
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=False, equal_oids=False)
#
#    def testTreeFromFilePosArgs(self):
#        self.assertRaises(TypeError, dendropy.Tree, StringIO(self.tree1_newick_str), "newick")
#
#    def testTreeFromFileMixedPosAndKeywordArgs(self):
#        self.assertRaises(TypeError, dendropy.Tree, StringIO(self.tree1_newick_str), format="newick")
#
#    def testTreeFromFilePosArgsWithNoFormat(self):
#        self.assertRaises(error.UnspecifiedFormatError, dendropy.Tree, stream=StringIO(self.tree1_newick_str), taxon_set=self.tree1.taxon_set)
#
#    def testTreeFromMultipleSource(self):
#        self.assertRaises(TypeError,
#                dendropy.Tree, \
#                StringIO(self.tree1_newick_str),
#                stream=StringIO(self.tree1_newick_str),
#                format="newick",
#                taxon_set=self.tree1.taxon_set)
#
#    def testTreeFromReadDistinctTaxa(self):
#        tree2 = dendropy.Tree()
#        tree2.read_from_string(self.tree1_newick_str, "newick")
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=True, equal_oids=False)
#
#    def testTreeFromReadSameTaxa(self):
#        tree2 = dendropy.Tree()
#        tree2.read_from_string(self.tree1_newick_str, "newick", taxon_set=self.tree1.taxon_set)
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=False, equal_oids=False)
#
#    def testTreeFromNewickReadIndexed(self):
#        nstr = "(A,(B,(C,D))); ((A,C),(B,D)); %s; (A,(C,(B,D))); ((A,D),(B,C));" % self.tree1_newick_str
#        tree2 = dendropy.Tree()
#        tree2.read_from_string(nstr, "newick", index=2, taxon_set=self.tree1.taxon_set)
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=False, equal_oids=False)
#
#    def testTreeFromNewickFileIndexed(self):
#        nstr = "(A,(B,(C,D))); ((A,C),(B,D)); %s; (A,(C,(B,D))); ((A,D),(B,C));" % self.tree1_newick_str
#        tree2 = dendropy.Tree(stream=StringIO(nstr), format="newick", index=2, taxon_set=self.tree1.taxon_set)
#        self.assertDistinctButEqual(self.tree1, tree2, distinct_taxa=False, equal_oids=False)

if __name__ == "__main__":
    unittest.main()