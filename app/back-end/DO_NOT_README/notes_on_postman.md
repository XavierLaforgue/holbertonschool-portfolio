# Notes on postman

## Using postman with wsl

I need to import/export postman files to work with them since there is no direct synchronization between the windows app and files located in wsl.

### Import

To import:

1. `ctrl + O` or `menu(hamburger to the top left of the UI) -> file -> import`
2. Select file or folders (for files in `wsl` the path starts with `\\wsl.localhost\`)

## Variables

To set variables in postman we have the following options:

```javascript
pm.environment.set("varName", varValue)
pm.collectionVariables.set("varName", varValue)
pm.variables.set("varName", varValue)
```

depending on the storing location:

- Environment for values that change according to the environment of execution: `dev`/`stage`/`prod`.
- Collection for values specific of the collection
- Local variables for values that will not persist beyond the current run
