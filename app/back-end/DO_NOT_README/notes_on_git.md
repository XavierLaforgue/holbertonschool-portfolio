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

A modern way to change the active branch is

```bash
git switch <branch-name>
# or, if we want to create and switch to a new branch:
git switch -c <new-branch-name>
```

We may even be able to switch branches with uncommitted changes.

To change the name of a branch we do

```bash
# if we are at the branch whose name we want to change
git branch -m <new-branch-name>
```

## Deleting branches

To delete a branch we need to be checking out a different branch, e.g., `dev`:

```bash
git switch dev
# to delete local branch:
git branch -d <branch-name>
# to force-delete the local branch even if it has unmerged changes:
git branch -D <branch-name>
# to delete a remote branch:
git push origin -d <branch-name>  # --delete === -d
```

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

## Stashing

when we made some changes but we do not want to commit them and we want to clean the worktree, we can stash the changes.

```bash
git stash -u -m "WIP put on the side"
```

where the `-u` includes the untracked files (it doesn't, by default) and `-m` gives a name/label to the stash.

When we are ready to bring forth the stashed changes we can do

```bash
git stash pop
# which brings forth the modifications and removes them from the stash
# or
git stash apply
# which applies the changes to the worktree without deleting them from the stash
```

## Adding line by line



## Unusual workflows to circunvent a bad practice

### Atomizing messy branch

**Situation:** I have made many changes into a branch, which do not correspond to the purpose of that branch.

**Chosen fix:** The messy feature branch being up to date with `dev` I:

<!-- markdownlint-disable MD029 -->
1. commit the changes, to "save" them in the messy branch, without pushing to `remote`;

```bash
# checking messy branch
git add .
git commit -m "Local savepoint. DO NOT PUSH"
```

2. create a backup branch to keep changes safely on the side before any other operation;

```bash
git branch backup/<messy-branch>
```

3. update the local `dev`;

```bash
git switch dev
git pull --ff-only
# --ff-only is a safety feature: it only updates the branch if it can be done cleanly by only fast-forwarding the commits
```

4. get back to the savepoint branch and recover the messy changes from it (NOT the backup);

```bash
git switch <messy-branch>
# git reset undoes commits
# --soft undoes them, brings them back to the workspace, but keeps them staged
# --mixed undoes them and brings them back to workspace unstaged, it is the default
# [DANGER!]: --hard undoes them and the changes ARE LOST definitively
# git reset --mixed HEAD~<number-of-savepoint-commits>
# or the perhaps safer option:
git reset --mixed dev
# this resets the messy branch to the state of dev
# to check what would that difference actually look like we can do 
# `git log dev..HEAD` and/or `git diff --stat dev` and/or `git diff dev` 
```

5. choose a meaningful set of related changes;
6. create a GitHub issue for their related feature;
7. create a branch for the issue, from `dev`;

```bash
git switch -c <new-feature> dev
```

8. make atomic commits to the new feature branch, using keywords and issue identifiers if applicable (`execute order 'close #66'`);

```bash
git add file1 file2 file3
git commit -m "Clean commit about new feature"
```

9. push to that branch;

```bash
git push -u origin <new-feature>
```

10. make and accept a PR from the new branch to `dev` (deleting the now-merged branch);
11. switch to `dev` and pull changes;

```bash
git switch dev
git pull --ff-only
```

12. cycle back to steps 5 through 10 until all changes have been merged into `dev`;

```bash
git switch -c <another-new-feature> dev
```

13. verify that `dev` is up-to-date with the savepoint branch;
14. delete messy branch
15. resume `GitHub Projects` workflow: create issue -> create related feature branch (`feature/feature-name`) -> commit to it until closing the issue -> PR to `dev` -> delete feature branch after accepting the PR -> restart.
<!-- markdownlint-enable MD029 -->
