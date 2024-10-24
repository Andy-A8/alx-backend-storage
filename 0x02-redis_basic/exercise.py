#!/usr/bin/env python3
"""
    0.Create a Cache class. In the __init__ method, store an instance of the
    Redis client as a private variable named _redis (using redis.Redis())
    and flush the instance using flushdb.
    Create a store method that takes a data argument and returns a string.

    1.Create a get method that take a key string argument and an optional
    Callable argument named fn. This callable will be used to convert
    the data back to the desired format.
    Implement 2 new methods: get_str and get_int that will automatically
    parametrize Cache.get with the correct conversion function.

    2.Implement a system to count how many times methods of the Cache class
    are called. Above Cache define a count_calls decorator that takes
    a single method Callable argument and returns a Callable. As a key,
    use the qualified name of method using the __qualname__ dunder method.
    Create and return function that increments the count for that key
    every time the method is called and returns the value returned by
    the original method.

    3.Define a call_history decorator to store the history of inputs and
    outputs for a particular function. In call_history, use the decorated
    function’s qualified name and append ":inputs" and ":outputs" to create
    input and output list keys, respectively. In the new function that the
    decorator will return, use rpush to append the input arguments

    4.Implement a replay function to display the history of calls of
    a particular function. Use keys generated in previous tasks to
    generate the given output.
"""


import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for decorated function: Increment count"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for the decoraated function: store history"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper

    def replay(fn: Callable):
        """Display the history of calls of a particular function"""
        r = redis.Redis()
        function_name = fn.__qualname__
        value = r.get(function_name)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0

            print("{} was called {} times:".format(function_name, value))

            inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

            outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

            for input, output in zip(inputs, outputs):
                try:
                    input = input.decode("utf-8")
                except Exception:
                    input = ""

                try:
                    output = output.decode("utf-8")
                except Exception:
                    output = ""

                print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """Create a Cache class"""

    def __init__(self):
        """store an instance of the Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key"""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[callable] = None) \
            -> Union[str, bytes, int, float]:
        """Convert the data back to the desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Automatically parametrize Cache.get with the correct
        conversion function"""
        value = self.__redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
