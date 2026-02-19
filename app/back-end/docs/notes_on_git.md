# Notes on `git`

## Update

To update `git` itself its repository must first be added:

```bash
sudo add-apt-repository ppa:git-core/ppa
```

Now, we can do

```bash
sudo apt update
sudo apt upgrade
```

To upgrade `git` to the latest stable version (check with `git --version`).

## Commits

`git` every-day commands: `add`, `commit`, and `push`.

```bash
# To stage (add to the 'index`) all modified files
git add .
# To stage specific files
git add filename1 filename2
# To commit the staged changes (optional arguments in square brackets)
git commit -m "CRUD message (short-clear title the changes)" [-m "Detailed description of the commit"]
git push
```

## Branches

To create a branch `dev` from the branch `main`:

```bash
git checkout -b dev main
```

After creating a new local branch we must update the remote repository.
When on the new branch, we can use

```bash
git push --set-upstream origin dev
```

to set it up and then commit the changes.

## Merging

In collaborative projects we would always use pull requests and never merges (upwards).
However, as this is a solo-project,  we can merge features to dev and I'll merge dev to main at least once.

Before merging upwards (towards `main`) it is recommended to merge the upper branch into the current branch to update current branch to latest upper branch.
Below, we assume we are merging a feature-branch to the dev branch.

```bash
# From any branch, update repository:
git fetch origin
# 'Move' to the branch that has the changes you want to merge, typically 'feature-branch' or 'dev':
git checkout feature-branch
# Merge changes that may have been applied to 'main' while working on the feature branch (mainly an issue while collaborating with other developers):
git merge origin/dev # or 'git merge main' if local 'main' is up-to-date
# resolve conflicts if any and push them:
git push origin feature-branch
```

Once the feature branch is up-to-date with 'dev', we merge it into 'dev':

```bash
# 'Move' to `dev` branch:
git checkout dev
# Merge your work to `dev`
git merge feature-branch
# Push the local changes to github:
git push origin dev
```
