/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React from 'react';
import Layout from '@theme/Layout';


function NotFound({location}) {
    const routing = {
        "/redirect-me" : "/still-not-found",
        "/docs/next/advanced/command_line_syntax" : "/docs/advanced/override_grammar/basic",
        "/docs/upgrades/version_base" : "/docs/upgrades/1.3_to_1.4/prepare_for_1_4",
        "/docs/next/upgrades/version_base" : "/docs/next/upgrades/1.3_to_1.4/prepare_for_1_4",
        "/docs/1.4/upgrades/version_base" : "/docs/1.4/upgrades/1.3_to_1.4/prepare_for_1_4",
        // TODO: activate redirect once 1.1 is released and is no longer the "next" version.  
        // "/docs/experimental/compose_api" : "/docs/advanced/compose_api",
    }

    const pathname = location.pathname.replace(/\/$/, "")
    if (routing[pathname] != null){
        window.location.replace(routing[pathname])
 	return
    }

  return (
    <Layout title="Page Not Found">
      <div className="container margin-vert--xl" data-canny>
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1 className="hero__title">Page Not Found</h1>
            <p>We could not find what you were looking for.</p>
            <p>
              Please contact the owner of the site that linked you to the
              original URL and let them know their link is broken.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default NotFound;
