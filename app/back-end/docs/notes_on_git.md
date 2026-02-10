# Notes on `git`

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

After creating a new local branch we must update the repote repository.
When on the new branch, we can commit changes and use

```bash
git push --set-upstream origin dev
```
