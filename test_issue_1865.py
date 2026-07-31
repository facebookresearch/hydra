import omegaconf
from hydra.utils import instantiate
from omegaconf import OmegaConf

class MyObject:
    def __init__(self, arg):
        self.arg = arg

omegaconf.OmegaConf.register_new_resolver("as_myobject", lambda arg: MyObject(arg))

class ClassA:
    def __init__(self, arg_A):
        self.arg_A = arg_A

class ClassB:
    def __init__(self, arg_B: MyObject):
        self.arg_B = arg_B

# Create config
config = OmegaConf.create({
    "vec": {
        "_target_": "__main__.ClassB",
        "arg_B": "${as_myobject:abc}"
    },
    "pipe": {
        "_target_": "__main__.ClassA",
        "arg_A": "${vec}"
    }
})

print("Testing instantiate(cfg)...")
try:
    result = instantiate(config)
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")

print("\nTesting instantiate(cfg.vec)...")
try:
    result = instantiate(config.vec)
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")

print("\nTesting instantiate(cfg.pipe)...")
try:
    result = instantiate(config.pipe)
    print("Success! (This should work but currently fails)")
except Exception as e:
    print(f"Failed with expected error: {type(e).__name__}")
    print(f"Error message: {e}")
