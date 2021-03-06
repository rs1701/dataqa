"""
Script to test plotting images
"""

import numpy as np
import os
import argparse
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from astropy.wcs import WCS
#import qa_continuum
import time


def main():
    start_time = time.time()

    # Create and parse argument list
    # ++++++++++++++++++++++++++++++
    parser = argparse.ArgumentParser(
        description='Create overview for QA')

    # Input path to fits file
    parser.add_argument("fits_file", type=str,
                        help='Input path to fits file')

    parser.add_argument("--output_file", type=str, default='',
                        help='Output path to fits file. Default current working directory')

    parser.add_argument("--vmin", type=float, default=0.05,
                        help='Min for logscale')

    parser.add_argument("--vmax", type=float, default=1000.,
                        help='Min for logscale')

    parser.add_argument("--symlog", action="store_true", default=False,
                        help='Enable sym log')

    args = parser.parse_args()

    fits_file = args.fits_file
    print("Reading {}".format(fits_file))

    if args.output_file == '':
        output_file = os.path.basename(fits_file).replace(
            ".fits", "_{0:.2f}_{1:.0f}.png".format(args.vmin, args.vmax))
    else:
        output_file = args.output_file
        output_file = output_file.replace(
            ".png", "_{0:.2f}_{1:.0f}.png".format(args.vmin, args.vmax))

    # get hdus
    fits_hdulist = fits.open(fits_file)

    # get WCS header of cube
    wcs = WCS(fits_hdulist[0].header)

    # remove unnecessary axis
    if wcs.naxis == 4:
        wcs = wcs.dropaxis(3)
        wcs = wcs.dropaxis(2)
        img = fits_hdulist[0].data[0][0]
    elif wcs.naxis == 3:
        wcs = wcs.dropaxis(2)
        img = fits_hdulist[0].data[0]
    else:
        img = fits_hdulist[0].data

    print("Plotting image")

    # set up plot
    ax = plt.subplot(projection=wcs)

    if args.symlog:
        output_file = output_file.replace(".png", "_symlog.png")
        fig = ax.imshow(
            img * 1.e3, norm=mc.SymLogNorm(1.e-3, vmin=args.vmin, vmax=args.vmax, clip=False),  origin='lower', interpolation="none")
    else:
        output_file = output_file.replace(".png", "_log.png")
        img[np.where(img < 1.e-9)] = 1.e-9
        fig = ax.imshow(
            img * 1.e3, norm=mc.LogNorm(vmin=args.vmin, vmax=args.vmax, clip=False),  origin='lower', interpolation="none")

    cbar = plt.colorbar(fig)
    cbar.set_label('Flux Density [mJy/beam]')

    # legend
    ax.coords[0].set_axislabel('Right Ascension')
    ax.coords[1].set_axislabel('Declination')
    ax.coords[0].set_major_formatter('hh:mm')

    ax.set_title("{0:s}".format(output_file.replace(".png", "")))

    print("Saving image as {}".format(output_file))
    plt.savefig(output_file, overwrite=True, bbox_inches='tight', dpi=300)


if __name__ == "__main__":
    main()
