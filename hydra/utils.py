import logging
import inspect

log = logging.getLogger(__name__)


def fullname(o):
    if inspect.isclass(o):
        return o.__module__ + "." + o.__qualname__
    else:
        return o.__module__ + "." + o.__class__.__qualname__


def get_class(path):
    try:
        from importlib import import_module
        module_path, _, class_name = path.rpartition('.')
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        return klass
    except ValueError as e:
        print("Error initializing class " + path)
        raise e


def get_static_method(full_method_name):
    try:
        spl = full_method_name.split('.')
        method_name = spl.pop()
        class_name = '.'.join(spl)
        clz = get_class(class_name)
        return getattr(clz, method_name)
    except Exception as e:
        log.error(f"Error getting static method {full_method_name} : {e}")
        raise e


def instantiate(config, *args):
    try:
        clazz = get_class(config['class'])
        return clazz(*args, **(config.params or {}))
    except Exception as e:
        log.error(f"Error instantiating {config.clazz} : {e}")
        raise e
