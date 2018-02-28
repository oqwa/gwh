GitWebHook
---
This is a simple Flask tool that will help you handle Git webhooks. Now it supports the following services:
* Bitbucket

Installation
---
```
pip install gwh
```

Basic usage
---
```python
import gwh

app = GitWebhook(host="127.0.0.1", port=8080)

@app.event(repository="oqwa/gwh", types=['push'], branches=['dev'])
def event():
    print(app.event_repository)
    print(app.event_type)
    print(app.pushed_branch)
    print(app.event_data)

app.run()
``` 

Feedback
---
Bug reports, feature requests, pull requests, any feedback, etc. are welcome. 