/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import React from 'react';
import classnames from 'classnames';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import withBaseUrl from '@docusaurus/withBaseUrl';
import styles from './styles.module.css';

const features = [
  {
    title: <>No boilerplate</>,
    imageUrl: 'img/undraw_docusaurus_mountain.svg',
    description: (
      <>
        Hydra let's you focus on the problem at hand, and not on boilerplate code like command line flags,
        Loading configuration files, logging etc.
      </>
    ),
  },
  {
    title: <>Powerful configuration</>,
    imageUrl: 'img/undraw_docusaurus_tree.svg',
    description: (
      <>
        With Hydra, you can compose your configuration dynamically, allowing you to easily
        get the perfect configuration for each run.
        You can override everything from the command line, which means you no longer need to maintain 10
        almost identical copies of your configuration file.
      </>
    ),
  },
  {
    title: <>Plugable architecture</>,
    imageUrl: 'img/Hydra-plugins.svg',
    description: (
      <>
          Hydra has a Pluggable architecture, allowing it to be to integrate with your own infrastructure.
          Future plugins will allow launching your code to AWS or other cloud providers directly from the command line.
      </>
    ),
  },
];

function Home() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Flexible experimentation framework">
      <header className={classnames('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className={classnames(
                'button button--outline button--secondary button--lg',
                styles.getStarted,
              )}
              to={withBaseUrl('docs/intro')}>
              Get Started
            </Link>
            <div className={styles.imageLogo}><img src="img/logo.svg"/></div>
          </div>
        </div>
      </header>
      <main>
        {features && features.length && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {features.map(({imageUrl, title, description}, idx) => (
                  <div
                    key={idx}
                    className={classnames('col col--4', styles.feature)}>
                    {imageUrl && (
                      <div className="text--center">
                        <img
                          className={styles.featureImage}
                          src={withBaseUrl(imageUrl)}
                          alt={title}
                        />
                      </div>
                    )}
                    <h3>{title}</h3>
                    <p>{description}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
    </Layout>
  );
}

export default Home;
