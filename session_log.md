# Session log: questions and abbreviated answers

Project: INF201 Week 43, Deliverable 2 (`Delivirable_2.ipynb`)

## Environment and files

**How do I activate the virtual environment?**
`source .venv/bin/activate` on macOS/zsh. In VS Code, pick the interpreter and notebook kernel from the `.venv`.

**How do I read a file's encoding?**
`file -I name`, or `chardet.detect(raw_bytes)` on a file opened in `"rb"` mode. Detection is a guess.

**chardet doesn't seem to work for the file.**
The snippet used the placeholder `"filename.txt"`. On the real data chardet works: all files are ASCII except `library_cafe/POS_02/register_sales.log`, which is UTF-8 (`Capøccino`) although chardet guessed MacRoman with low confidence. Read all logs as UTF-8.

**How does `iterdir` work?**
`Path.iterdir()` yields the direct children (files and folders) of a directory as `Path` objects, in arbitrary order. It is not recursive.

**PosixPath to string?**
`str(path)` or `os.fspath(path)`. `path.name`, `.stem`, `.suffix` give parts.

## JSON and pandas basics

**How do I traverse a JSON file?**
`json.load` gives dicts and lists. Loop through `config["regions"]`, then `stores`, then `registers`, or write a recursive walker. Config names (`Library Cafe`) differ from folder names (`library_cafe`).

**How do I sort a DataFrame?**
`df.sort_values("col")`, `ascending=False`, several columns, or `sort_index()`. Convert strings to numbers or datetimes first.

**What is a timedelta?**
A length of time (difference between two datetimes). Use `total_seconds()`, not `.seconds`. In pandas: `pd.Timedelta`, `.diff()`.

**What's wrong with `dataframe.resample(timedelta=timedelta(hours=1))`?**
The parameter is `rule` (not `timedelta`), it needs a datetime index or `on=`, and it needs an aggregation such as `.sum()`.

## Debugging `sum_total_per_item_per_hour`

Errors found, in the order they appeared:
- `KeyError: 'time'`: `groupby("item").sum()` removed the time column before `resample`.
- Prices were strings, so `.sum()` concatenated them. Fixed by `float(...)`.
- `TypeError: Only valid with DatetimeIndex`: resampling after the sum used item names as the index.
- `ValueError: No axis named TimeGrouper`: the two groupers were not in a list. Use `groupby(["item", pd.Grouper(freq="1h")])`.
- Missing `return`; the function only printed.

## Analysis questions

**Sum all successful, refunded and cancelled transactions in the file** (`library_cafe/POS_02`, 80 valid lines):
SUCCESS 3216.70 (51), REFUND 68.40 (15), CANCELLED 2048.61 (14). Five `999.00` glitch prices and mixed currencies inflate these.

**Refund ratio per item** (`refund / (sales + 10**-6)`, same file):
Cappuccino 0.125, Croissant 0.5, Espresso 0.1, Latte 0.2143, Muffin 1.0, Sandwich 0.3333.

**How do I get column values from the pivot table?**
`pivot["SUCCESS"]`, `.to_numpy()`, `.tolist()`, `pivot.loc[row, col]`. Rows and columns are `pivot.index` and `pivot.columns`.

**What's wrong with `refund_ratio_per_item`?**
It never computed a ratio, printed instead of returning, hard-coded "Cappuccino", looked up `["Cappuccino"]` in a table with a `price` column level, and called a `compute_refund_ratio` that used `np.size`.

**Why can't I get the success count from the table?**
`status` is the row index, not a column. Use `.loc["SUCCESS"]`.

**Can I get the names from the table?**
`table.columns` for items, `table.index` for statuses. With two column levels use `get_level_values(1)`.

**`cannot assign without a target object`**
`df.query("status = 'REFUND'")` used one `=`. Use `==`.

**What am I doing wrong with the groupby?**
A `groupby` alone is a lazy object; it needs `.size()`, `.sum()` etc. `sales[item]` selects a column, not a group.

**Can you pivot without aggregating?**
`df.pivot(...)` works only when each index/column pair is unique. Otherwise use `pivot_table`, `groupby().unstack()` or `pd.crosstab`.

**`Grouper for 'item' not 1-dimensional`**
Real error, from `pivot_table(columns="item", values="item")`, which used `item` twice. Use `values="price"` or `pd.crosstab`.

## General Python and pandas tips

- Get a property from every element: list comprehension, `[row["price"] for row in log]`.
- Replace a column with an array: `df["col"] = arr` (same length, assigned by position, so order must match).
- Print without omitting values: `pd.set_option("display.max_rows", None)`, `np.set_printoptions(threshold=sys.maxsize)`.
- Limit displayed rows: `.head(n)`, `groupby(...).head(n)`, `display.max_rows`.
- Rename a result column: `.agg(price=("price", "sum"))` or `.rename(columns=...)`.

## Git

**How do I push this to an existing GitHub repo?**
`git init`, add `.gitignore` (exclude `.venv/`), commit, `git remote add origin <url>`, `git push -u origin main`. If the remote already has commits, pull with `--allow-unrelated-histories` first.

**Best-practice `.gitignore`**
Created `.gitignore` (virtual environments, Python caches, build output, Jupyter checkpoints, `.env`, editor and macOS files). `*.log` and `Data/` were left out on purpose.

## Review of the solutions

**Critical bug:** cleaned prices were assigned by position to a DataFrame that had been sorted by time, so about 716 of 720 rows got another transaction's price. This affected all output files.

**Fixed:** cell 9 now writes the cleaned prices back into the records before building the DataFrame. Verified on all 720 rows: 0 mismatches, 0 values of `999.00` left.

**Still to do:**
- Re-run cell 9 to regenerate `cleaned_transactions.csv`, `hourly_revenue.json`, `status_pivot_table.csv` and `item_refund_ratios.csv`, which were written before the fix.
- Check the NOK × 10 conversion against the task text; EUR and USD are not converted.
- `all_active_registers` is computed but never used.
- `item_refund_ratios.csv` has a space in the header (`item, refund_ratio`).
- Remove `sklearn==0.0` and unused packages from `requirements.txt`.
- `refund_ratio_per_item` raises `KeyError` if there is no `REFUND` or `SUCCESS` column.
