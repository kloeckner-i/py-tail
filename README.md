# py-tail

A Python library for tailing files.

## Usage

### File Reading Follower

```python
from follower import Follower

def main():
    with Follower("yourlogfile.log") as f:
        for line in f.lines():
            print(line)

if __name__ == "__main__":
    main()
```
