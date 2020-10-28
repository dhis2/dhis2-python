#!/usr/bin/env python

import dhis2.core.logging  # noqa


def main():
    from .core.cli import cli

    cli(obj={})


if __name__ == "__main__":
    main()
