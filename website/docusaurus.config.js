/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

module.exports = {
    title: 'Hydra',
    tagline: 'A framework for elegantly configuring complex applications',
    url: 'https://hydra.cc',
    baseUrl: '/',
    favicon: 'img/Hydra-head.svg',
    organizationName: 'facebookresearch', // Usually your GitHub org/user name.
    projectName: 'hydra', // Usually your repo name.
    themeConfig: {
        googleAnalytics: {
          trackingID: 'UA-149862507-1',
        },
        algolia: {
          apiKey: '8e04f3376c4e6e060f9d8d56734fa67b',
          indexName: 'hydra',
          algoliaOptions: {},
        },
        navbar: {
            title: 'Hydra',
            logo: {
                alt: 'Hydra logo',
                src: 'img/logo.svg',
            },
            links: [
                {to: 'docs/intro', label: 'Docs', position: 'left'},
                {to: 'versions', label: 'Versions', position: 'left'},
                {to: 'https://github.com/facebookresearch/hydra', label: 'Hydra@GitHub', position: 'left'},
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    items: [
                        {
                            label: 'Docs',
                            to: 'docs/intro'
                        },
                        {
                            label: 'Hydra@GitHub',
                            to: 'https://github.com/facebookresearch/hydra',
                        },
                        {
                            label: 'Powered by OmegaConf',
                            to: 'https://github.com/omry/omegaconf',
                        },
                    ],
                },
            ],
            logo: {
                alt: 'Facebook Open Source Logo',
                src: 'https://docusaurus.io/img/oss_logo.png',
            },
            copyright: `Copyright © ${new Date().getFullYear()} Facebook, Inc.`,
        },
    },
    presets: [
        [
            '@docusaurus/preset-classic',
            {
                docs: {
                    sidebarPath: require.resolve('./sidebars.js'),
                    showLastUpdateAuthor: true,
                    showLastUpdateTime: true,
                    editUrl: 'https://github.com/facebookresearch/hydra/edit/master/website/',
                },
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            },
        ],
    ],
};
