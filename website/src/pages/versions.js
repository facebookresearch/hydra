import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';

import versions from '../../versions.json';

function Versions() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  const latestVersion = versions[0];

  return (
    <Layout permalink="/versions">
      <div className="container margin-vert--xl">
       <h1>{siteConfig.title} Versions</h1>
        <div className="margin-bottom--lg">
          <h3 id="latest">Current version (Stable)</h3>
          <ul>
      <li><b>{latestVersion}</b> <Link to={useBaseUrl('/docs/intro')}>Documentation</Link></li>
          </ul>
          <h3 id="rc">Latest Version</h3>
          <p>Here you can find the latest documentation and unreleased code.</p>
          <ul>
      <li><b>Next Release</b> <Link to={useBaseUrl('/docs/next/intro')}>Documentation</Link></li>
          </ul>
          <h3 id="archive">Past Versions</h3>
          <p>
            Here you can find documentation for previous versions of Hydra.
          </p>
          <ul>
              {versions.map(
                version =>
                  version !== latestVersion && (
                      <li>{version} <Link to={useBaseUrl(`/docs/${version}/intro`)}>Documentation</Link></li>))}
           </ul>
         </div>
      </div>
   </Layout>
  );
};


Versions.title = 'Versions';
export default Versions;

