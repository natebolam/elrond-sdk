import logging
import pprint
from argparse import ArgumentParser

from erdpy import builder, dependencies, projects, errors

logger = logging.getLogger("cli")


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = setup_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
    else:
        args.func(args)


def setup_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    install_parser = subparsers.add_parser("install")
    choices = ["C_BUILDCHAIN", "SOL_BUILDCHAIN", "RUST_BUILDCHAIN", "NODE_DEBUG"]
    install_parser.add_argument("group", choices=choices)
    install_parser.set_defaults(func=install)

    create_parser = subparsers.add_parser("new")
    create_parser.add_argument("name")
    create_parser.add_argument("--template", required=True)
    create_parser.add_argument("--directory", type=str)
    create_parser.set_defaults(func=create)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("project")
    build_parser.add_argument("--debug", action="store_true")
    build_parser.set_defaults(func=build)

    return parser


def install(args):
    group = args.group

    try:
        dependencies.install_group(group, overwrite=True)
    except errors.KnownError as err:
        logger.fatal(err)


def create(args):
    name = args.name
    template = args.template
    directory = args.directory

    try:
        projects.create_project(name, template, directory)
    except errors.KnownError as err:
        logger.fatal(err)


def build(args):
    project = args.project
    debug = args.debug

    builder.build_project(project, debug)


if __name__ == "__main__":
    main()
