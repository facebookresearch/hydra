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
        Hydra lets you focus on the problem at hand instead of spending time on boilerplate code like command line flags, loading configuration files, logging etc.
      </>
    ),
  },
  {
    title: <>Powerful configuration</>,
    imageUrl: 'img/undraw_docusaurus_tree.svg',
    description: (
      <>
        With Hydra, you can compose your configuration dynamically, enabling you to easily
        get the perfect configuration for each run.
        You can override everything from the command line, which makes experimentation fast, and removes the need to maintain multiple similar configuration files.
      </>
    ),
  },
  {
    title: <>Pluggable architecture</>,
    imageUrl: 'img/Hydra-plugins.svg',
    description: (
      <>
          Hydra has a pluggable architecture, enabling it to integrate with your infrastructure.
          Future plugins will enable launching your code on AWS or other cloud providers directly from the command line.
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
      description="A framework for elegantly configuring complex applications">
      <header className={classnames('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
          <div className={styles.imageLogo}><img src="img/logo.svg"/></div>
            <Link
              className={classnames(
                'button button--outline button--secondary button--lg',
                styles.getStarted,
              )}
              to={withBaseUrl('docs/intro')}>
              Get Started
            </Link>
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
