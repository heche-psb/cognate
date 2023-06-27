#!/usr/bin/python3
import click
import logging
import sys
import os
import warnings
from timeit import default_timer as timer
import pkg_resources
from rich.logging import RichHandler
__version__ = pkg_resources.require("orthomason")[0].version


# cli entry point
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--verbosity', '-v', type=click.Choice(['info', 'debug']),
    default='info', help="Verbosity level, default = info.")
def cli(verbosity):
    """
    OrthoMason - Copyright (C) 2023-2024 Hengchi Chen\n
    Contact: heche@psb.vib-ugent.be
    """
    logging.basicConfig(
        format='%(message)s',
        handlers=[RichHandler()],
        datefmt='%H:%M:%S',
        level=verbosity.upper())
    logging.info("This is OrthoMason v{}".format(__version__))
    pass


# Find fossils
@cli.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('data', type=click.Path(exists=True))
@click.option('--tmpdir', '-tm', default=None, show_default=True, help='temporary working directory')
@click.option('--outdir', '-o', default='find_ortho', show_default=True, help='output directory')
@click.option('--to_stop', is_flag=True, help="don't translate through STOP codons")
@click.option('--cds', is_flag=True, help="enforce proper CDS sequences")
@click.option('--evalue', '-e', default=1e-10, help="e-value cut-off for similarity")
@click.option('--nthreads', '-n', default=4, show_default=True,help="number of threads to use")
def find(**kwargs):
    """
    Find orthologues
    """
    _find(**kwargs)

def _find(data,tmpdir,outdir,to_stop,cds,evalue,nthreads):
    from orthomason.ortho import cdsortho
    start = timer()
    cdsortho(data,tmpdir,outdir,to_stop,cds,evalue,nthreads)
    end = timer()
    logging.info("Total run time: {}s".format(int(end-start)))

if __name__ == '__main__':
    cli()