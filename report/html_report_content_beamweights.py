import os
import sys
from astropy.table import Table, join
import logging
import glob
import time
import socket
import numpy as np

logger = logging.getLogger(__name__)


def write_obs_content_beamweights(html_code, qa_report_obs_path, page_type, obs_info=None):
    """Function to create the html page for beamweights

    Args:
        html_code (str): HTML code with header and title
        qa_report_obs_path (str): Path to the report directory
        page_type (str): The type of report page
        obs_info (list(str)): Basic information of observation

    Return:
        html_code (str): Body of HTML code for this page
    """

    logger.info("Writing html code for page {0:s}".format(page_type))

    if obs_info is not None:
        obs_id = obs_info['Obs_ID'][0]
        source_list = np.array(
            [obs_info['Target'][0], obs_info['Flux_Calibrator'][0], obs_info['Pol_Calibrator'][0]])
    else:
        obs_id = os.path.basename(qa_report_obs_path)
        source_list = ''

    html_code += """
        <div class="w3-container w3-large">
            <p>
                Here you can inspect the beamweights per beam for different subbands for the calibrator used in this observation: {0:s}. For each individual beam, you can click your way through the subbands using the back and forward arrows. The thin top arrows allow you to step through every single image while the thick bottom arrows change between every 10th image. When you reach the last image, it starts at the beginning.
                These plots should be the same for observations which used the same calibrator. 
            </p>
            <h4> Note: Due to issues with getting the script to extract the beam weights, creating the beamweights plots has been temporarily disabled </h4>
        </div>\n
        """.format(source_list[1])

    # total number of beams
    n_beams = 40

    qa_report_obs_page_path = os.path.join(qa_report_obs_path, page_type)

    # Create html code for image galleries
    # ====================================

    # get beams
    beam_list = glob.glob(
        "{0:s}/{1:s}/[0-3][0-9]".format(qa_report_obs_path, page_type))

    if len(beam_list) != 0:

        html_code += """
                <div class="w3-container w3-margin-top">\n"""

        # get a list of beam numbers
        #beam_nr_list = np.array([os.path.basename(beam) for beam in beam_list])

        # get a list of reference beams
        beam_nr_list = np.array(
            ["{0:02d}".format(beam) for beam in range(n_beams)])

        # go through the beams
        for beam_counter in range(n_beams):

            # get a list of all images to make sure that at least one exists
            image_list = glob.glob(
                "{0:s}/{1:s}/{2:02d}/*.png".format(qa_report_obs_path, page_type, beam_counter))

            # to properly make the gallery, open the row
            if beam_counter % 4 == 0:
                html_code += """<div class="w3-row w3-margin-top">\n"""

            # check that there are images for this beam
            if len(image_list) != 0:

                # sort the list
                image_list.sort()

                # create the slideshow for this beam
                # open the slideshow div
                html_code += """
                        <div class="w3-content w3-display-container w3-quarter w3-border">\n"""

                # go through each plot and add elements to the slideshow
                # the first element gets a different class value
                html_code += """
                            <a href="{0:s}/{1:02d}/{2:s}">
                                <img name="slideshow{1:d}" class="w3-show" src="{0:s}/{1:02d}/{2:s}" style="width:100%">
                             </a>\n""".format(page_type, beam_counter, os.path.basename(image_list[0]))

                for image_counter in range(1, len(image_list)):
                    html_code += """
                            <a href="{0:s}/{1:02d}/{2:s}">
                                <img name="slideshow{1:d}" class="w3-hide" src="{0:s}/{1:02d}/{2:s}" style="width:100%">
                            </a>\n""".format(page_type, beam_counter, os.path.basename(image_list[image_counter]))

                # write the caption
                html_code += """
                            <div class="w3-container w3-center">
                                <h5 name="slideshow_label{0:d}">Beam {0:02d}, Subband {1:s}</h5>
                            </div>""".format(beam_counter, os.path.basename(image_list[0]).split("_")[3].replace("S", ""))

                # write the buttons
                html_code += """
                            <button class="w3-button w3-display-topleft" onclick="change_slide(-1, 'slideshow{0:d}', 'slideshow_label{0:d}')">&#10092;</button>
                            <button class="w3-button w3-display-topright" onclick="change_slide(1, 'slideshow{0:d}', 'slideshow_label{0:d}')">&#10093;</button>
                            <button class="w3-button w3-display-bottomleft" onclick="change_slide(-10, 'slideshow{0:d}', 'slideshow_label{0:d}')">&#10096;</button>
                            <button class="w3-button w3-display-bottomright" onclick="change_slide(10, 'slideshow{0:d}', 'slideshow_label{0:d}')">&#10097;</button>\n""".format(beam_counter)

                # close the slideshow div
                html_code += """</div>\n"""
            else:
                html_code += """
                        <div class="w3-content w3-display-container w3-quarter">
                            <img src="" alt="No image for beam {0:s}", width="100%">
                        </div>\n""".format(beam_nr_list[beam_counter])

            # close the row
            if beam_counter % 4 == 3 or beam_counter == len(beam_nr_list):
                html_code += """</div>\n"""

        html_code += """</div>\n"""

        # html_code += """
        #     <div class="gallery" name="{0:s}">
        #         <p class="warning">
        #             No plots and validation tool were found for {1:s}
        #         </p>
        #     </div>\n""".format(button_html_name, page_type)

    else:
        logger.warning("No beams for beamweights found")
        html_code += """
        <div class="w3-container w3-large w3-text-red w3-margin-top">
            <p>
                No beams were found for beamweidhts.
            </p>
        </div\n"""

    return html_code
