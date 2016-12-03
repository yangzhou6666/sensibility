#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
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

import argparse
import io
import json
import subprocess
from pathlib import Path

from keras.models import model_from_json

THIS_DIRECTORY = Path(__file__).parent
TOKENIZE_JS_BIN = ('node', str(THIS_DIRECTORY / 'tokenize-js'))

parser = argparse.ArgumentParser()
parser.add_argument('filename', nargs='?', type=Path,
                    default=Path('/dev/stdin'))
parser.add_argument('--architecture', type=Path,
                    default=THIS_DIRECTORY / 'model-architecture.json')
parser.add_argument('--weights-forwards', type=Path,
                    default=THIS_DIRECTORY / 'javascript-tiny.5.h5')


def tokenize_file(file_obj):
    """
    >>> import tempfile
    >>> with tempfile.TemporaryFile('w+t', encoding='utf-8') as f:
    ...     f.write('$("hello");')
    ...     f.seek(0)
    ...     tokens = tokenize_file(f)
    11
    0
    >>> len(tokens)
    5
    """
    status =subprocess.run(TOKENIZE_JS_BIN,
                           check=True,
                           stdin=file_obj,
                           stdout=subprocess.PIPE)
    return json.loads(status.stdout.decode('UTF-8'))


class Model:
    """
    >>> model = Model.from_filenames(architecture='model-architecture.json',
    ...                              weights='javascript-tiny.5.h5')
    """
    def __init__(self, model):
        self.model = model

    @classmethod
    def from_filenames(cls, *, architecture=None, weights=None):
        with open(architecture) as archfile:
            model = model_from_json(archfile.read())
        model.load_weights(weights)

        return cls(model)



if __name__ == '__main__':
    globals().update(vars(parser.parse_args()))

    assert architecture.exists()
    assert weights_forwards.exists()

    with open(str(filename), 'rt', encoding='UTF-8') as script:
        raw_tokens = tokenize_file(script)

    forwards = Model.from_filenames(architecture=architecture,
                                    weights=weights_forwards)

    # TODO: create sentences for the file
    # TODO: Predict the next token with the model.
    # TODO: Compare with actual (this is like validation!)