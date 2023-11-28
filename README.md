<p align="center"><img src="https://raw.githubusercontent.com/facebookresearch/hydra/main/website/static/img/Hydra-Readme-logo2.svg" alt="logo" width="70%" /></p>

<p align="center">
  <a href="https://pypi.org/project/hydra-core/">
    <img src="https://img.shields.io/pypi/v/hydra-core" alt="PyPI" />
  </a>
  <a href="https://circleci.com/gh/facebookresearch/hydra">
    <img src="https://img.shields.io/circleci/build/github/facebookresearch/hydra?token=af199cd2deca9e70e53776f9ded96284b10687e9" alt="CircleCI" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/pypi/l/hydra-core" alt="PyPI - License" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/pypi/pyversions/hydra-core" alt="PyPI - Python Version" />
  </a>
  <a href="https://pepy.tech/project/hydra-core?versions=0.11.*&versions=1.0.*&versions=1.1.*">
    <img src="https://pepy.tech/badge/hydra-core/month" alt="Downloads" />
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
  </a>
  <a href="https://lgtm.com/projects/g/facebookresearch/hydra/alerts/">
    <img src="https://img.shields.io/lgtm/alerts/g/facebookresearch/hydra.svg?logo=lgtm&logoWidth=18" alt="Total alerts" />
  </a>
  <a href="https://lgtm.com/projects/g/facebookresearch/hydra/context:python">
    <img src="https://img.shields.io/lgtm/grade/python/g/facebookresearch/hydra.svg?logo=lgtm&logoWidth=18" alt="Language grade: Python" />
  </a>
  <p align="center">
    <i>A framework for elegantly configuring complex applications.</i>
  </p>
  <p align="center">
    <i>Check the <a href="https://hydra.cc/">website</a> for more information,<br>
    or click the thumbnail below for a one-minute video introduction to Hydra.</i>
  </p>
  <p align="center">
   <a href="http://www.youtube.com/watch?feature=player_embedded&v=Slc3gRQpnBI" target="_blank">
     <img src="http://img.youtube.com/vi/Slc3gRQpnBI/hqdefault.jpg" alt="1 minute overview" width="240" height="180" border="10" />
   </a>
  </p>
</p>

----------------------


### Releases

#### Stable

**Hydra 1.3** is the stable version of Hydra.
- [Documentation](https://hydra.cc/docs/1.3/intro/)
- Installation : `pip install hydra-core --upgrade`

See the [NEWS.md](NEWS.md) file for a summary of recent changes to Hydra.

### License
Hydra is licensed under [MIT License](LICENSE).

## Hydra Ecosystem

#### Check out these third-party libraries that build on Hydra's functionality:
* [hydra-zen](https://github.com/mit-ll-responsible-ai/hydra-zen): Pythonic utilities for working with Hydra. Dynamic config generation capabilities, enhanced config store features, a Python API for launching Hydra jobs, and more.
* [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template): user-friendly template combining Hydra with [Pytorch-Lightning](https://github.com/Lightning-AI/lightning) for ML experimentation.
* [hydra-torch](https://github.com/pytorch/hydra-torch): [configen](https://github.com/facebookresearch/hydra/tree/main/tools/configen)-generated configuration classes enabling type-safe PyTorch configuration for Hydra apps.
* NVIDIA's DeepLearningExamples repository contains a Hydra Launcher plugin, the [distributed_launcher](https://github.com/NVIDIA/DeepLearningExamples/tree/9c34e35c218514b8607d7cf381d8a982a01175e9/Tools/PyTorch/TimeSeriesPredictionPlatform/distributed_launcher), which makes use of the pytorch [distributed.launch](https://pytorch.org/docs/stable/distributed.html#launch-utility) API.

#### Ask questions in Github Discussions or StackOverflow (Use the tag #fb-hydra or #omegaconf):
* [Github Discussions](https://github.com/facebookresearch/hydra/discussions)
* [StackOverflow](https://stackexchange.com/filters/391828/hydra-questions)
* [Twitter](https://twitter.com/Hydra_Framework)

Check out the Meta AI [blog post](https://ai.facebook.com/blog/reengineering-facebook-ais-deep-learning-platforms-for-interoperability/) to learn about how Hydra fits into Meta's efforts to reengineer deep learning platforms for interoperability.

### Citing Hydra
If you use Hydra in your research please use the following BibTeX entry:
```BibTeX
@Misc{Yadan2019Hydra,
  author =       {Omry Yadan},
  title =        {Hydra - A framework for elegantly configuring complex applications},
  howpublished = {Github},
  year =         {2019},
  url =          {https://github.com/facebookresearch/hydra}
}
```

