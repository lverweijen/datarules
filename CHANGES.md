### Version 0.1.1 ###

Add `datatest.utilities` with function `toposort`.

### Version 0.1.0 ###

- Get rid of `Runner`.
- Add `CorrectionList` and `CorrectionList`. They implement the methods that were formerly on Runner.
- Replace `load_checks` by `CheckList.from_file`.
- Replace `load_corrections` by `CorrectionList.from_file`.
- Add `Context` to supply extra data.
- Rename `Check.condition` to `Check.test`.

### Version 0.0.3 ###

- Add some basic safety precautions.

### Version 0.0.2 ###

- Refactor `Check` and `Condition`.
- Experiment with different ways of writing `Check` in examples.
- CheckFails is now a class.
- Drop function `report.print_tracebacks()`.
