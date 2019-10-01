/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

(function() {
  const src = 'facebookresearch.github.io/hydra';
  const dst = 'cli.dev';
  if (window.location.href.indexOf(src) > -1) {
    var fragments = window.location.href.split(src);
    var newLocation = fragments[0] + dst + fragments[1];
    window.location = newLocation + (newLocation.endsWith('/') ? '' : '/');
  }
})();
