# deadlock-server


## How to run
```
uvicorn main:app --reload
```

## How to print logs
```python
import logging
logger = logging.getLogger(__name__)
logger.warning("Hi")
```
