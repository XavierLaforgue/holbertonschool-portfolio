# Notes on bash

Print to the standard output with `echo` or `printf`.

## `echo`

Use double quotes for the strings to be expanded (the variable values evaluated).
Next to punctuation is safer to use curly brackets: `${VAR_NAME}`
Use flag `-e` to enable interpretation of backslashes.

```bash
echo "Dropping database $DB_NAME"
echo "Dropping database ${DB_NAME}."
echo -e "Dropping $DB_NAME \nDatabase owner (${DB_USER}) will be requested"
```

## `printf`

`printf` is may be, however, more predictable.
Use `man printf` for manual.
Basic syntax:

```bash
printf 'String in single quotes does not evaluate variables like ${PWD}'
printf "String in double quotes does evaluate variables like ${PWD}"
export $FUNC_NAME='printf'
printf 'Both, single quote and double quote'\''s syntax, use the format controls of same-name %s\n' "C function: (${FUNC_NAME})"
export $DOUBLE='double'
printf "The arguments are written as strings separated by spaces after the format string, choosing between %s quotes or %s quotes depending on the need to evaluate variables\n" '$single' "$DOUBLE" 
```
