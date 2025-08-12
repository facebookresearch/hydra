/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

const {fbContent} = require('docusaurus-plugin-internaldocs-fb/internal');

module.exports = {
    title: 'Hydra',
    tagline: 'A framework for elegantly configuring complex applications',
    url: 'https://hydra.cc',
    baseUrl: '/',
    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',
    trailingSlash: true,
    favicon: 'img/Hydra-head.svg',
    organizationName: 'facebookresearch', // Usually your GitHub org/user name.
    projectName: 'hydra', // Usually your repo name.
    customFields: {
        githubLinkVersionToBaseUrl: {
            // TODO: Update once a branch is cut for 1.4
            "1.4": "https://github.com/facebookresearch/hydra/blob/main/",
            "1.3": "https://github.com/facebookresearch/hydra/blob/1.3_branch/",
            "1.2": "https://github.com/facebookresearch/hydra/blob/1.2_branch/",
            "1.1": "https://github.com/facebookresearch/hydra/blob/1.1_branch/",
            "1.0": "https://github.com/facebookresearch/hydra/blob/1.0_branch/",
            current: "https://github.com/facebookresearch/hydra/blob/main/",
        },
    },
    themeConfig: {
        announcementBar: {
            id: 'support_ukraine',
            content:
              'Support Ukraine 🇺🇦 <a target="_blank" rel="noopener noreferrer" href="https://opensource.fb.com/support-ukraine"> Help Provide Humanitarian Aid to Ukraine</a>.',
            backgroundColor: '#20232a',
            textColor: '#fff',
            isCloseable: false,
        },
        algolia: {
            appId: 'KVTVP1D78C',
            apiKey: '9585f41bc128c5a99dd9f22827e1e836',
            indexName: 'hydra',
            algoliaOptions: {},
        },
        // announcementBar: {
        //   id: 'supportus',
        //   content:
        //     '⭐️ If you like Hydra, give it a star on <a target="_blank" rel="noopener noreferrer" href="https://github.com/facebookresearch/hydra">GitHub</a>! ⭐️',
        // },
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
                            to: 'blog'
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
                        {
                            label: 'Cookies',
                            href: 'https://opensource.facebook.com/legal/cookie-policy',
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
            copyright: `Copyright © ${new Date().getFullYear()} Meta Platforms, Inc`,
        },
    },
    presets: [
        [
            require.resolve('docusaurus-plugin-internaldocs-fb/docusaurus-preset'),
            {
                docs: {
                    sidebarPath: require.resolve('./sidebars.js'),
                    showLastUpdateAuthor: fbContent({
                        internal: false,
                        external: true,
                    }),
                    showLastUpdateTime: fbContent({
                        internal: false,
                        external: true,
                    }),
                    editUrl: 'https://github.com/facebookresearch/hydra/edit/main/website/',
                    lastVersion: 'current',
                },
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
                googleAnalytics: {
                    trackingID: 'UA-149862507-1',
                },
            },
        ],
    ],
};
