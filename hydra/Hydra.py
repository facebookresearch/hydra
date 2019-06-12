import logging
import logging.config
import os
from time import strftime, localtime

from omegaconf import OmegaConf

def configure_log(cfg, verbose=None):
    """
    :param cfg:
    :param verbose: all or root to activate verbose logging for all modules, otherwise a comma separated list of modules
    :return:
    """
    # configure target directory for all logs files (binary, text. models etc)
    log_dir_suffix = cfg.log_dir_suffix or strftime("%Y-%m-%d_%H-%M-%S", localtime())
    log_dir = os.path.join(cfg.log_dir or "logs", log_dir_suffix)
    cfg.full_log_dir = log_dir
    os.makedirs(cfg.full_log_dir, exist_ok=True)

    logcfg = OmegaConf.from_filename(os.path.abspath(cfg.log_config))
    log_name = logcfg.handlers.file.filename
    if not os.path.isabs(log_name):
        logcfg.handlers.file.filename = os.path.join(cfg.full_log_dir, log_name)
    logging.config.dictConfig(logcfg)

    global log
    log = logging.getLogger(__name__)

    if verbose:
        if verbose in ('all', 'root'):
            logging.getLogger().setLevel(logging.DEBUG)
            verbose = 'root'
        for logger in verbose.split(','):
            logging.getLogger(logger).setLevel(logging.DEBUG)

    log.info(f"Saving logs to {cfg.full_log_dir}")

def hydra():
    print("Hydra main")




if __name__ == '__main__':
    hydra()