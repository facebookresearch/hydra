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
    plugins: [require.resolve('docusaurus-plugin-internaldocs-fb')],
    themeConfig: {
        googleAnalytics: {
            trackingID: 'UA-149862507-1',
        },
        algolia: {
            apiKey: '8e04f3376c4e6e060f9d8d56734fa67b',
            indexName: 'hydra',
            algoliaOptions: {},
        },
        announcementBar: {
          id: 'supportus',
          content:
            '⭐️ If you like Hydra, give it a star on <a target="_blank" rel="noopener noreferrer" href="https://github.com/facebookresearch/hydra">GitHub</a>! ⭐️',
        },        
		prism: {
		  additionalLanguages: ['antlr4'],
		},
        navbar: {
            title: 'Hydra',
            logo: {
                alt: 'Hydra logo',
                src: 'img/logo.svg',
            },
            items: [
                {to: 'docs/intro', label: 'Docs', position: 'left'},
                {position: 'left', type: 'docsVersionDropdown'},
                {to: 'blog', label: 'Blog', position: 'left'},
                {to: 'https://github.com/facebookresearch/hydra', label: 'Hydra@GitHub', position: 'left'},
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: "Links",
                    items: [
                        {
                            label: 'Blog',
                            to: 'Blog'
                        },
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
                {
                    title: 'Legal',
                    // Please do not remove the privacy and terms, it's a legal requirement.
                    items: [
                        {
                            label: 'Privacy',
                            href: 'https://opensource.facebook.com/legal/privacy/',
                            target: '_blank',
                            rel: 'noreferrer noopener',
                        },
                        {
                            label: 'Terms',
                            href: 'https://opensource.facebook.com/legal/terms/',
                            target: '_blank',
                            rel: 'noreferrer noopener',
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
