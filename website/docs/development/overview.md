---
id: overview
title: Overview
sidebar_label: Overview
---

This guide assumes you have forked and checked-out the [repository](https://github.com/facebookresearch/hydra).
It is recommended that you install Hydra in a virtual environment like [conda](https://docs.conda.io/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/).

## Environment setup
Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and create an empty Conda environment with:
```
conda create -n hydra38 python=3.8 -y
```

<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
The core Hydra framework supports Python 3.6 or newer. You may need to create additional environments for different Python versions if CI detect issues on a supported version of Python.
</div>
<br/>

Activate the environment:
```
conda activate hydra38
```
From the source tree, install Hydra in development mode with the following command:
```
pip install -r requirements/dev.txt -e .
```