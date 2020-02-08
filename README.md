# HonestHalls

- `honesthalls/` is the base Django project directory.
- `honesthalls/halls/` is the Django app for the project.
- `honesthalls/halls/templates/` contains the HTML templates.
- `honesthalls/halls/static/` contains static resources (CSS, JS).

### Running the project
- Clone the repo.
- `cd` into `first_group_project/`
- Run `pipenv shell` to start a shell in the project environment (can install pipenv with `pip install pipenv`)
- To install Django and other dependencies, run `pipenv install`
- `cd` into `honesthalls/` (dir with manage.py)
- Run `python manage.py runserver` to start the server (default port is 8000)

### *Remember to work on your own feature branch*
- To create a new branch make sure you are on `master` (`git checkout master`) and run `git checkout -b new-branch`
- To checkout an existing branch do `git checkout existing-branch`
- Never push or commit directly into `master`
- To push your own branch do `git push origin existing-branch`
- To request your changes to be merged into `master` go to the [Branches tab](https://gitlab.cs.man.ac.uk/f07893fm/first_group_project/branches) in GitLab and make a *Merge Request*.
- Before sending a merge request, make sure to update your own branch with the latest changes from master.
```bash
git checkout master # Switch to master
git fetch origin # Update master from origin (the remote repo)
git checkout exisiting-brach # Go to your feature branch
git merge origin/master # Merge master in it to update it
# Fix any conflicts and make sure that everything runs fine.
# Open https://gitlab.cs.man.ac.uk/f07893fm/first_group_project/merge_requests/new and create the merge request
```

### *Always test your code before commiting and run linters on it*
- To check PEP8 compilance run `pycodestyle .` in the root project dir.

### Requirements
- Python v3.8
- Pipenv