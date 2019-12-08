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
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

const features = [
  {
    title: <>No boilerplate</>,
    imageUrl: 'img/undraw_site_content_hydra_plain.svg',
    description: (
      <>
        Hydra lets you focus on the problem at hand instead of spending time on boilerplate code like command line flags, loading configuration files, logging etc.
      </>
    ),
  },
  {
    title: <>Powerful configuration</>,
    imageUrl: 'img/undraw_product_teardown_hydra_plain.svg',
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
          {/* Left */}
          <div className={styles.heroLeft}>
            <div className={styles.imageLogo}><img src="img/logo.svg" /></div>
          </div>
          {/* Right */}
          <div className={styles.heroRight}>
            <h1 className={"hero__title"}>{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttonContainer}>
              <div className={styles.buttons}>
                <Link
                  className={classnames(
                    'button button--success button--lg',
                    styles.getStarted,
                  )}
                  to={useBaseUrl('docs/intro')}>
                  Get Started
                </Link>
                <span className={styles['index-ctas-github-button']}>
                  <iframe
                    src="https://ghbtns.com/github-btn.html?user=facebookresearch&amp;repo=hydra&amp;type=star&amp;count=true&amp;size=large"
                    frameBorder={0}
                    scrolling={0}
                    width={160}
                    height={30}
                    title="GitHub Stars"
                  />
                </span>
              </div>
            </div>
          </div>

        </div>
      </header>
      <main>
        {features && features.length && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {features.map(({imageUrl, title, description}, idx) => (
                  <div key={idx} className={'col col--4'}>
                    <div className={styles.feature}>
                      {imageUrl && (
                        <div className={styles.thumbnail}>
                          <img
                            className={styles.featureImage}
                            src={useBaseUrl(imageUrl)}
                            alt={title}
                          />
                        </div>
                      )}
                      <h3 className="feature">{title}</h3>
                      <p>{description}</p>
                    </div>
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
