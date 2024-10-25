# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
import subprocess
import sys


# The following tests are testing that the app actually runs as expected
# when installed and executed from the command line.
# You don't need to repeat those tests in your own app.
class TestAppOutput:
    # Testing the Hydra app as an executable script
    # This only works if we are at the root of the hydra-app-example
    def test_python_run(self, tmpdir: str) -> None:
        self.verify_output(
            subprocess.check_output(
                [
                    sys.executable,
                    "hydra_app/main.py",
                    f'hydra.run.dir="{tmpdir}"',
                    "app.user=test_user",
                ]
            )
        )

    # Testing the Hydra app as a console script
    def test_installed_run(self, tmpdir: str) -> None:
        self.verify_output(
            subprocess.check_output(
                ["hydra_app", f'hydra.run.dir="{tmpdir}"', "app.user=test_user"]
            )
        )

    # test that installed app configs are loaded via pkg://hydra_app.conf
    def test_installed_run_searchpath(self, tmpdir: str) -> None:
        output = subprocess.check_output(["hydra_app", "--info"]).decode("utf-8")
        assert re.search(re.escape("pkg://hydra_app.conf"), output) is not None

    @staticmethod
    def verify_output(result: bytes) -> None:
        assert str(result.decode("utf-8")).strip() == "Hello test_user, 10 + 20 = 30"
