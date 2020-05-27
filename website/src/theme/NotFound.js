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
        "/redirect-me" : "/still-not-found"
    }
    if (routing[location.pathname] != null){
        window.location.href = routing[location.pathname]
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