# Step 0
## Pre-Commit Hooks

Run the below code right after clone this repo from your terminal.
```
pip install -r common.txt
```

```
pre-commit install
```
The steps ensure to work pre commit hooks before you push the code to the repo.
By running "pre-commit install", it executes .pre-commit-config.yaml file, then, the yaml file sets up the git hook scripts.
After the command, 'pre-commit' runs automatically on "git commit"
<p align="center">
  <img src="images/pre-commit.png" alt="pre-commit" width="400" height="300">
</p>
The picture is actually running for this repo. So, the file checks 7 points (6 ids under the hooks and black)
Once, you change code on this repo and commit the changes through <br>

- git commit -m 'First Commit' on terminal <br>
- Click the "Commit" panel (the left side on Pycharm) <br>

Either way, it runs automatically like the below figure.
<p align="center">
  <img src="images/pre-commit-results.png" alt="pre-commit-results" width="500" height="200">
</p>

More information about
pre-commit: https://pre-commit.com/
black: https://github.com/psf/black

*additional material for code convention:
Docstring: https://peps.python.org/pep-0257/
Type Hints: https://peps.python.org/pep-0484/
Unit Test: https://docs.python.org/3/library/unittest.html and start with test_


# Step 1
