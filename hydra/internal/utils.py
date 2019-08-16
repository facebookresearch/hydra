import re
from time import strftime, localtime

from omegaconf import OmegaConf


class Utils:
    @staticmethod
    def get_valid_filename(s):
        s = str(s).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", s)


def setup_globals():
    try:
        OmegaConf.register_resolver(
            "now", lambda pattern: strftime(pattern, localtime())
        )

        def job_error(x):
            raise Exception(
                "job:{} is no longer available. use hydra.job.{}".format(x, x)
            )

        OmegaConf.register_resolver("job", job_error)

    except AssertionError:
        # calling it again in no_workers mode will throw. safe to ignore.
        pass
