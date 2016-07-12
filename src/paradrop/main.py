'''
Core module. Contains the entry point into Paradrop and establishes all other modules.
Does not implement any behavior itself.
'''

import argparse

from paradrop.shared import nexus, settings


def main(args_string=None):
    p = argparse.ArgumentParser(prog='Paradrop', description='Paradrop API server running on client')

    p.add_argument('-s', '--settings', help='Overwrite settings, format is "KEY:VALUE"',
                   action='append', type=str, default=[])
    p.add_argument('--config', help='Run as the configuration daemon',
                   action='store_true')
    p.add_argument('--mode', '-m', help='Set the mode to one of [development, production, test, local]',
                   action='store', type=str, default='production')

    # Things to replace
    p.add_argument('--local', '-l', help='Run on local machine', action='store_true')
    p.add_argument('--development', help='Enable the development environment variables',
                   action='store_true')

    # No longer used
    p.add_argument('--unittest', help="Run the server in unittest mode", action='store_true')
    p.add_argument('--verbose', '-v', help='Enable verbose', action='store_true')

    args = p.parse_args()

    # Temp- this should go to nexus (the settings portion of it, at least)
    # Change the confd directories so we can run locally
    if args.local:
        settings.PDCONFD_WRITE_DIR = "/tmp/pdconfd"
        settings.UCI_CONFIG_DIR = "/tmp/config.d"
        settings.HOST_CONFIG_PATH = "/tmp/hostconfig.yaml"

    # Check for settings to overwrite
    settings.updateSettings(args.settings)

    # Globally assign the nexus object singleton
    nexus.core = nexus.NexusBase(args.mode, settings=args.settings, stealStdio=True, printToConsole=True)

    if args.config:
        from paradrop.confd import main

        # Start the configuration daemon
        main.run_pdconfd()

    else:
        from paradrop.confd import main
        from paradrop import backend

        # Start the configuration service as a thread
        main.run_thread()

        # Now setup the RESTful API server for Paradrop
        backend.server.setup(args)

if __name__ == "__main__":
    main()
