# urlmonitor
Solution for monitoring of URLs and design allowing to extend with actions.

The project is not created for actual use-case. I created it to refresh my Python knowledge and to test several Dev and DevOps concepts in Python:

* Abstract base classes (ABC)
* Subject-Observer pattern. Health monitor is the subject and is notifying a list of observers performing actions (OS command, API call, etc.)
* Async IO (asyncio, aiohttp)
* Implement hooks for quality: branch naming, linters (pylint, mypy), pytest, coverage, password detection
* Testing async code
* VSCode config for Python development

It is WIP. camelCase is used instead of snake_case. Required minimal Pyton versions is 3.8, but code will probably run on 3.7 as well.

## How to run

After cloning the repository and creation of virual environment:

```
# Run the code
pip install -r requirements.txt
python3 src/main.py

# Development
git checkout -b feature/new-feature
python3 init-repo.py
pip install -r requirements-dev.txt
```

Config files:
* conf-urls.json: List of URLs to be monitored. Multiple configuration options available.
* conf-osa_urls.txt: List of URLs for each to execute an action OS command when notified by the Monitor
* conf-apia_urls.txt: List of URLs for each to execute an action API call when notified by the Monitor
