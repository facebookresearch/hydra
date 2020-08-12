---
id: extended
title: Extended Override syntax
---
## Overview
Hydra supports a set of functions in the command line.

Functions are defined as `function_name(param1,...paramn)`.
When calling a function, one can optionally name parameters. This is following the Python convention of naming parameters.
The function:
```python
def func(param1:int, param2:str) -> bool:
    ...
```
Can be called in the following forms:
```python
func(10,foo)                 # Positional only
func(10,param2=foo)          # Mixed positional and named
func(param1=10,param2=foo)   # Named only
func(param1=10,foo)          # error: positional argument follows keyword argument
```
Note lack of quotes in the examples above. Despite some similarities, this is not Python.

:::important
Hydra supports very specific functions. If you would like to have
another function added please file an issue and explain the use case.
:::

## Sweeps
Sweepers are using sweeps to determine what to do. For example, one can instruct the basic sweeper to sweep over all
combinations of the lists `num1=range(0,3)` `num2=range(0,3)`, which will result in `9` jobs, each getting a 
different pair of numbers from `0`, `1` and `2`.

### Choice sweep
#### Signature
```python
def choice(
    *args: Union[str, int, float, bool, Dict[Any, Any], List[Any], ChoiceSweep]
) -> ChoiceSweep:
    """
    A choice sweep over the specified values
    """
```
#### Examples
Choice sweeps are the most common sweeps.
A choice sweep is described in one of two equivalent forms.
```yaml
db=mysql,postgresql          # a comma separated list of two or more elements. 
db=choice(mysql,postgresql)  # choice
```
### Glob choice sweep
#### Signature
```python
def glob(
    include: Union[List[str], str], exclude: Optional[Union[List[str], str]] = None
) -> Glob:
    """
    A glob selects from all options in the config group.
    inputs are in glob format. e.g: *, foo*, *foo.
    :param include: a string or a list of strings to use as include globs
    :param exclude: a string or a list of strings to use as exclude globs
    :return: A Glob object
    """
```
#### Examples
Assuming the config group schema with the options school, support and warehouse:
```yaml
schema=glob(*)                                # school,support,warehouse
schema=glob(*,exclude=support)                # school,warehouse
schema=glob([s*,w*],exclude=school)           # support,warehouse
```

### Range sweep
#### Signature
```python
def range(
    start: Union[int, float], stop: Union[int, float], step: Union[int, float] = 1
) -> RangeSweep:
    """
    Range is defines a sweeep over a range of integer or floating point values.
    For a positive step, the contents of a range r are determined by the formula
     r[i] = start + step*i where i >= 0 and r[i] < stop.
    For a negative step, the contents of the range are still determined by the formula
     r[i] = start + step*i, but the constraints are i >= 0 and r[i] > stop.
    """
```
#### Examples
```yaml
num=range(0,5)                        # 0,1,2,3,4
num=range(0,5,2)                      # 0,2,4
num=range(0,10,3.3)                   # 0.0,3.3,6.6,9.9
```

### Interval sweep
An interval sweep represents all the floating point value between two values.
This is used by optimizing sweepers like Ax and Nevergrad. The basic sweeper does not support interval.
 
#### Signature
```python
def interval(start: Union[int, float], end: Union[int, float]) -> IntervalSweep:
    """
    A continuous interval between two floating point values.
    value=interval(x,y) is interpreted as x <= value < y
    """
```
#### Examples
```yaml
#interval(1.0,5.0)  # 1.0 <= x < 5.0
#interval(1,5)      # 1.0 <= x < 5.0, auto-cast to floats
```

### Tag

#### Signature
Tagging allows advanced sweepers to add arbitrary metadata to a sweep.
```python
def tag(*args: Union[str, Union[Sweep]], sweep: Optional[Sweep] = None) -> Sweep:
    """
    Tags the sweep with a list of string tags.
    """
```
#### Examples
```yaml
#tag(log,interval(0,1))          # 1.0 <= x < 1.0, tags=[log]
#tag(foo,bar,interval(0,1))      # 1.0 <= x < 1.0, tags=[foo,bar]
```

## Reordering lists and sweeps

### sort
#### Signature
```python
def sort(
    *args: Union[ElementType, ChoiceSweep, RangeSweep],
    sweep: Optional[Union[ChoiceSweep, RangeSweep]] = None,
    list: Optional[List[Any]] = None,
    reverse: bool = False,
) -> Any:
    """
    Sort an input list or sweep.
    reverse=True reverses the order
    """
```
#### Examples
```yaml
# sweep
sort(1,3,2)                         # ChoiceSweep(1,2,3)
sort(1,3,2,reverse=true)            # ChoiceSweep(3,2,1)
sort(choice(1,2,3))                 # ChoiceSweep(1,2,3)
sort(sweep=choice(1,2,3))           # ChoiceSweep(1,2,3)
sort(choice(1,2,3),reverse=true)    # ChoiceSweep(3,2,1)
sort(range(10,1))                   # range in ascending order
sort(range(1,10),reverse=true)      # range in descending order

# lists
sort([1,3,2])                       # [1,2,3]
sort(list=[1,3,2])                  # [1,2,3]
sort(list=[1,3,2], reverse=true)    # [3,2,1]

# single value returned as is
sort(1)                             # 1
```

### shuffle
#### Signature
```python
def shuffle(
    *args: Union[ElementType, ChoiceSweep, RangeSweep],
    sweep: Optional[Union[ChoiceSweep, RangeSweep]] = None,
    list: Optional[List[Any]] = None,
) -> Union[List[Any], ChoiceSweep, RangeSweep]:
    """
    Shuffle input list or sweep (does not support interval)
    """
```
#### Examples
```yaml
shuffle(a,b,c)                                       # shuffled a,b,c
shuffle(choice(a,b,c)), shuffle(sweep=choice(a,b,c)) # shuffled choice(a,b,c)
shuffle(range(1,10))                                 # shuffled range(1,10)
shuffle([a,b,c]), shuffle(list=[a,b,c])              # shuffled list [a,b,c] 
```

## Type casting
Casts an input to int, float, bool or str.
#### Signature
```python
def cast_int(*args: CastType, value: Optional[CastType] = None) -> Any
def cast_float(*args: CastType, value: Optional[CastType] = None) -> Any
def cast_bool(*args: CastType, value: Optional[CastType] = None) -> Any
def cast_str(*args: CastType, value: Optional[CastType] = None) -> Any
```

#### Examples
```yaml
int(3.14)                  # 3 (int)
float(10)                  # 10.0 (float)
str(10)                    # "10" (str)
bool(1)                    # true (bool)
float(range(1,10))         # range(1.0,10.0)
str([1,2,3])               # ['1','2','3']
str({a:10})                # {a:'10'}
```

### Conversion matrix
Below is the conversion matrix from various inputs to all supported types.
Input are grouped by type.

[//]: # (Convertion matrix source: https://docs.google.com/document/d/1JDZGHKk4PrZHqsTTS6ao-DQOu2eVD4ULR6uAxVUR-WI/edit#)

|                    	| int()       	| float()           	| str()             	| bool()                	|
|--------------------	|-------------	|-------------------	|-------------------	|-----------------------	|
|         10         	| 10          	| 10.0              	| “10”              	| true                  	|
|          0         	| 0           	| 0.0               	| “0”               	| false                 	|
|        10.0        	| 10          	| 10.0              	| “10.0”            	| true                  	|
|         0.0        	| 0           	| 0.0               	| “0.0”             	| false                 	|
|         inf        	| error       	| inf               	| ‘inf’             	| true                  	|
|         nan        	| error       	| nan               	| ‘nan’             	| true                  	|
|         1e6        	| 1,000,000   	| 1e6               	| ‘1000000.0’       	| true                  	|
|         foo        	| error       	| error             	| foo               	| error                 	|
|  “” (empty string) 	| error       	| error             	| “”                	| error                 	|
|        “10”        	| 10          	| 10.0              	| “10”              	| error                 	|
|       “10.0”       	| error       	| 10.0              	| “10.0”            	| error                 	|
|       “true”       	| error       	| error             	| “true”            	| true                  	|
|       “false”      	| error       	| error             	| “false”           	| false                 	|
|      “[1,2,3]”     	| error       	| error             	| “[1,2,3]”         	| error                 	|
|      “{a:10}”      	| error       	| error             	| “{a:10}”          	| error                 	|
|        true        	| 1           	| 1.0               	| “true”            	| true                  	|
|        false       	| 0           	| 0.0               	| “false”           	| false                 	|
|         []         	| []          	| []                	| []                	| []                    	|
|       [0,1,2]      	| [0,1,2]     	| [0.0,1.0,2.0]     	| [“0”,”1”,”2”]     	| [false,true,true]     	|
|       [1,[2]]      	| [1,[2]]     	| [1.0,[2.0]]       	| [“1”,[“2”]]       	| [true,[true]]         	|
|        [a,1]       	| error       	| error             	| [“a”,”1”]         	| [true,true]           	|
|         {}         	| {}          	| {}                	| {}                	| {}                    	|
|       {a:10}       	| {a:10}      	| {a:10.0}          	| {a:”10”}          	| true                  	|
|     {a:[0,1,2]}    	| {a:[0,1,2]} 	| {a:[0.0,1.0,2.-]} 	| {a:[“0”,”1”,”2”]} 	| {a:[false,true,true]} 	|
|    {a:10,b:xyz}    	| error       	| error             	| {a:”10”,b:”xyz”}  	| error                 	|
|     choice(0,1)    	| choice(0,1) 	| choice(0.0,1.0)   	| choice(“0”,“1”)   	| choice(false,true)    	|
|     choice(a,b)    	| error       	| error             	| choice(“a”,”b”)   	| choice(true,true)     	|
|     choice(1,a)    	| error       	| error             	| choice(“1”,”a”)   	| choice(true,true)     	|
| interval(1.0, 2.0) 	| error       	| error             	| error             	| error                 	|
|     range(1,10)    	| range(1,10) 	| range(1.0,10.0)   	| error             	| error                 	|
|  range(1.0, 10.0)  	| range(1,10) 	| range(1.0,10.0)   	| error             	| error                 	|

