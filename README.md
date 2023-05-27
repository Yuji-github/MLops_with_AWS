# Step 0
## Pre-Commit Hooks

Run the below 2 codes right after clone this repo from your terminal.
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

More information about <br>
pre-commit: https://pre-commit.com/ <br>
black: https://github.com/psf/black <br>

*additional material for code convention: <br>
Docstring: https://peps.python.org/pep-0257/ <br>
Type Hints: https://peps.python.org/pep-0484/ <br>
Unit Test: https://docs.python.org/3/library/unittest.html and start with test_ <br>


# Step 1
## Jenkins
Before downloading, Jenkins should check your PC system. <br>
If you don't have JAVA, you need to download JAVA and Git Bah. <br>
Then you check [System properties -> Environment Variables -> path], System variables has JAVA-HOME and right Path condition. <br>

### How to run Jenkins at localhost
- Download Jenkins <br>
1. Run the below code from your terminal(Pycharm)

```
java -jar jenkins.war
```
2. C:\Users\User\Desktop(Jenkins folder location) >java -jar jenkins.war
3. Open browser, Type below port number for Jenkins

```

localhost:8080
```
When using Jenkins, do steps 1, 2 and 3 every time. <br>

### How to ues Jenkins
When you open the dashboard, click New Item <br>

<p>
<img src="images/Jenkins-page.png" alt="Jenkins" width="400" height="300">
</p>

Look at the picture above <br>

- An item name = your project name
- Click Pipeline

Next step is What do you want to build. <br>

Please follow the picture below
<p>
<img src="images/jenkins-configure1.png" alt="Jenkins-configure1" width="400" height="300">
</p>

What do you want to run
- Set ***** (every minute) run

<p>
<img src="images/jenkins-configure2.png" alt="Jenkins-configure2" width="400" height="300">
</p>

Make Pipeline script
- Click try sample pipeline

<p>
<img src="images/jenkins-configure3.png" alt="Jenkins-configure3" width="400" height="300">
</p>
