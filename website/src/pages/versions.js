// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
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
                    <ul>
                        <li><Link to={useBaseUrl(`/docs/intro`)}>Stable version : (<b>{latestVersion}</b>)</Link></li>
                        <li><Link to={useBaseUrl('/docs/next/intro')}>Next version (<b>master</b>)</Link></li>
                    </ul>
                    {versions.length > 1 && <h3 id="archive">Past Versions</h3>}
                    {<ul>{
                        versions.filter(function (v) {return v != latestVersion}).map(
                            version => (
                                <li>{version} <Link to={useBaseUrl(`/docs/${version}/intro`)}>Documentation</Link></li>)
                        )
                    }
                    </ul>
                    }
                </div>
            </div>
        </Layout>
    );
};


Versions.title = 'Versions';
export default Versions;

