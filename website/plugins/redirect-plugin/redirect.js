/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import siteConfig from '@generated/docusaurus.config';

(function() {
  const src = `${siteConfig.organizationName}.github.io/${siteConfig.projectName}`;
  const dst = siteConfig.url.split('//')[1];

  if (window.location.href.indexOf(src) > -1) {
    const fragments = window.location.href.split(src);
    const newLocation = fragments[0] + dst + fragments[1];
    window.location = newLocation + (newLocation.endsWith('/') ? '' : '/');
  }
})();
