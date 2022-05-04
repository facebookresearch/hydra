## Setting up a new testing AMI for ray launcher.

To run the tool:

- Make sure the dependencies in `setup_integration_test_ami.py` matches exactly ray launcher's `setup.py`.
- Install AWS CLI, check AWS documentation for more details.
- Before running the tool, set up your aws profile with admin access to the Hydra test AWS account.
```
AWS_PROFILE=jieru python create_integration_test_ami.py
```
You will see a new AMI created in the output
```commandline
ec2.Image(id='ami-0d65d5647e065a180') current state pending
...
```
Sometimes it could take hours for a new AMI to be created. Proceed to the next step once the 
AMI becomes available.

- Update the `AWS_RAY_AMI` env variable in `tests/test_ray_aws_launcher.py`
- Run the test locally and debug if needed.
- Create a PR and make sure all CI pass!
