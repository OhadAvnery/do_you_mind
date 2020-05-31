[![Build Status](https://travis-ci.com/OhadAvnery/do_you_mind.svg?branch=master)](https://travis-ci.com/OhadAvnery/do_you_mind)
[![Documentation Status](https://readthedocs.org/projects/do-you-mind/badge/?version=latest)](https://do-you-mind.readthedocs.io/en/latest/?badge=latest)
[![CodeCov](https://i.imgur.com/l7YTBgz.png)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)


# doyoumind

A package responsible for uploading user snapshots, parsing them and visualising the results. 
See [full documentation](https://do-you-mind.readthedocs.io/en/latest).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/OhadAvnery/do_you_mind.git
    ...
    $ cd do_you_mind
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [doyoumind] $ # oooweeee!
    ```

3. There aren't really any tests, but if you'd like to see a green dot, run:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `doyoumind` packages provides the following classes:

- `client`

    This class encapsulates the concept of `foo`, and returns `"foo"` when run.

    In addition, it provides the `inc` method to increment integers, and the
    `add` method to sum them.

    ```pycon
    >>> from foobar import Foo
    >>> foo = Foo()
    >>> foo.run()
    'foo'
    >>> foo.inc(1)
    2
    >>> foo.add(1, 2)
    3
    ```

- `Bar`

    This class encapsulates the concept of `bar`; it's very similar to `Foo`,
    except it returns `"bar"` when run.

    ```pycon
    >>> from foobar import Bar
    >>> bar = Bar()
    >>> bar.run()
    'bar'
    ```

The `foobar` package also provides a command-line interface:

```sh
$ python -m foobar
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m foobar foo run
foo
$ python -m foobar foo inc 1
2
$ python -m foobar foo add 1 2
3
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `foobar`, not `foo` or
`bar`.

```sh
$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```
