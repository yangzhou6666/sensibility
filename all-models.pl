#!/usr/bin/env perl

# Copyright 2017 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


use strict;

my $folds = 5;      # Zero-indexed.
my $sigmoid = 300;
my $sentence = 20;
my $max_epoch = 5;  # One-indexed.
my $max_files = 128; # Arbitrary upper bound!
my $max_fold = $folds - 1;

print "# Autogenerated file: do not modify!\n";

# Create declare the phony rules.
print "PHONY: models mutations\n";

# Create a phony rule for models.
print "models:";
foreach my $fold (0 .. $max_fold) {
    foreach my $dir ('f', 'b') {
        print " \$(CORPUS)-$dir-$sigmoid-$sentence.$fold.$max_epoch.h5";
    }
}
print "\n";

# Create rules for the initial trained models.
foreach my $direction ('forwards', 'backwards') {
    my $dir = substr $direction, 0, 1;
    foreach my $fold (0 .. $max_fold) {
        print "\$(CORPUS)-$dir-$sigmoid-$sentence.$fold.1.h5: \$(ASSIGNED_VECTORS)\n";
        print "\t./train new --$direction --fold $fold \$<\n";
    }
}
print "\n";

# Create prefix rules for rest of the training.
foreach my $epoch (2 .. $max_epoch) {
    my $last_epoch = $epoch - 1;
    print "%.$epoch.h5: %.$last_epoch.h5\n";
    print "\t./train continue \$(ASSIGNED_VECTORS) \$<\n";
}


###
print "\n";
###

# Create a phony rule for mutations.
print "mutations:";
foreach my $fold (0 .. $max_fold) {
    print " \$(CORPUS).$fold.$max_epoch.cookie";
}
print "\n";

# Create rules for mutations.
foreach my $fold (0 .. $max_fold) {
    print "\$(CORPUS).$fold.$max_epoch.cookie:";
    print " \$(CORPUS)-f-$sigmoid-$sentence.$fold.$max_epoch.h5";
    print " \$(CORPUS)-b-$sigmoid-$sentence.$fold.$max_epoch.h5";
    print " \$(TEST_SET).$fold";
    print "\n";
    print "\t./mutate.py -n $max_files \$(ASSIGNED_VECTORS) \$< \$(TEST_SET).$fold\n";
}
print "\n";
