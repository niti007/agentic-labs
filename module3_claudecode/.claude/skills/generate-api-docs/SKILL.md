---
name: generate-api-docs
description: Generate Markdown API documentation for Python modules. Use when the user asks to document functions, produce API docs, or create a reference for a module's public interface.
---

# Generate API Docs

Reusable workflow: turn a Python module's public functions into clean Markdown
reference docs. Invoke once, get consistent output across any project.

## Steps
1. Identify the target module(s). If none given, ask or default to `src/`.
2. For each **public** function (no leading underscore):
   - Read its signature and docstring.
   - Extract: name, parameters (with types), return type, summary.
3. Emit one Markdown section per function:

```markdown
### `function_name(param: type, ...) -> return_type`
One-line summary from the docstring.

**Parameters**
- `param` (type) — description

**Returns:** description
```

4. Group functions by file, with the file path as an `##` heading.
5. Write the result to `docs/API.md` (create the folder if needed) unless the
   user asks for a different location.

## Notes
- Skip private helpers (names starting with `_`).
- If a function lacks a docstring, flag it as `_(undocumented)_` rather than
  inventing one.
