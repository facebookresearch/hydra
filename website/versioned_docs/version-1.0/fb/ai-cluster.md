---
id: internal-fb-cluster
title: Hydra on the internet FB Cluster
---

Support for launching jobs to the AI cluster is currently still experimental and is expected to evolve over
the coming months.

## flow-cli

flow-cli integration is hacky at the moment.
See the the sample f6.sample_projects.classy_hydra_project.workflow.main for details.

```bash title="Example run"
$ CFG='{"config": {"overrides": ["trainer=multi_gpu","trainer.max_epochs=90","+lr_scheduler=multi_step"]}}'
$ ENTITLEMENT=cv_images_gpu_prod
$ TEAM=team_computer_vision
$ WORKFLOW=f6.sample_projects.classy_hydra_project.workflow.main
$ flow-cli canary $WORKFLOW --run-as-secure-group $TEAM --parameters-json=$CFG --entitlement $ENTITLEMENT
```

## fry
TODO
