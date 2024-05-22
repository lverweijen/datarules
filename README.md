# pymodify
Data cleaning tools in python

This is still a work in progress.
The idea of the project is to create similar tools as can be found on https://github.com/data-cleaning/, but to use python instead of R.

Reasons to make this:
- If most of your data cleaning pipeline is already in python, this avoids needing to switch to a different language.
- It avoids needing to learn R. Instead you can fully harness the power of pandas for data cleaning, which is great if you already have learned pandas and want to apply your existing knowledge.
- This can be used to prove that Python has the same data manipulation capabilities as R.

There are a few challenges:
- The original package heavily makes use of code rewriting and code analysis. Although python supports this, this is more commonly done in R than in python and there might be reasons for that.
- The original package relies heavily on `eval`. This requires the rules to be safe and sanitized. (This is probably also a problem in R).
- Handling of `NA`'s is arguably more straightforward in R than in pandas. R has native support for nullable booleans. In pandas, support for nullable booleans is more limited.

Status:

The original R packages are the following:

- [dcmodify](https://github.com/data-cleaning/dcmodify)
- [validate](https://github.com/data-cleaning/validate)
- [editrules](https://github.com/data-cleaning/editrules)
- [errorlocate](https://github.com/data-cleaning/errorlocate)
- [deductive](https://github.com/data-cleaning/deductive)

The first one (dcmodify) seems most straightforward to do in python and I have already made a start working on it (which I will upload later).
The other ones seem more challenging for now.

This is a work in progress and should only be used on your own risk. Contributions are appreciated. I'm also interested in alternative ideas. Maybe a completely different approach could work better in python.
