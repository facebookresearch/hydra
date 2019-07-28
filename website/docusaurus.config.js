/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

module.exports = {
    title: 'Hydra',
    tagline: 'Flexible experimentation framework',
    url: 'https://fairinternal.github.io/',
    baseUrl: '/hydra',
    favicon: 'img/favicon.ico',
    organizationName: 'fairinternal', // Usually your GitHub org/user name.
    projectName: 'hydra', // Usually your repo name.
    themeConfig: {
        navbar: {
            title: 'Hydra',
            logo: {
                alt: 'Hydra logo',
                src: 'img/logo.svg',
            },
            links: [
                {to: 'docs/intro', label: 'Docs', position: 'left'},
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: 'Docs',
                    items: [
                        {
                            label: 'Docs',
                            to: 'docs/intro',
                        },
                    ],
                },
            ],
            logo: {
                alt: 'Facebook Open Source Logo',
                src: 'https://docusaurus.io/img/oss_logo.png',
            },
            copyright: `Copyright © ${new Date().getFullYear()} Facebook, Inc. Built with Docusaurus.`,
        },
    },
    presets: [
        [
            '@docusaurus/preset-classic',
            {
                docs: {
                    sidebarPath: require.resolve('./sidebars.js'),
                },
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            },
        ],
    ],
};
