# local_cache
A python local_cache wrapper
## usage
```python
from local_cache import cache


@cache(60 * 10, max_len=10000)
def test_cache(string):
    return 'foo'
```
