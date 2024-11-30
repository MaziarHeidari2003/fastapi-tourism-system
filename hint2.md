# Here I  want to write about the challenges and solutions

**returning empty dicts in the resevev flight endpoint**

```python

    return {
        "order_code": order,
        "tickets": tickets,
       "passengers": [p.name for p in passengers]
    }

# this is the return of the code

```

- Lets solve it using pydantic models!