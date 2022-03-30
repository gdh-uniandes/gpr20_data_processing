"""Data processing module for GPR-20.

This module provides the implementation of the GPR-20 data processing
pipline. The pipeline includes the parsing of the VNA raw responses and
the storage of the data.
"""

from gpr20_data_processing.data_parsing import DataParsing
from gpr20_data_processing.data_storage import DataStorage


class DataProcessing(object):
    """Implementation of the processing pipeline for the GPR-20 data.
    
    This class provides the implementation that wraps-up the data processing
    pipeline for the GPR-20 robot. The processing pipeline is implemented in
    other classes but instantiated in this one. Depending on the processing
    requirements, futher stages can be added to this pipeline.
    """

    @staticmethod
    def process_data(survey_dir, x_coord, y_coord, z_coord, antennae_height,
                     timestamp, survey_id, sample_id, vna_freq, vna_trace):
        """Process the VNA data and store it in persistent storage.

        Args:
            survey_dir (str): folder in which the data will be stored in. The
                path is relative to the main data folder.
            x_coord (float): coordinate for the X axis in which the data was
                acquired.
            y_coord (float): coordinate for the Y axis in which the data was
                acquired.
            z_coord (float): coordinate for the Z axis in which the data was
                acquired.
            antennae_height (float): antennae height as measured in the
                location in which the data was acquired.
            timestamp (str): timestamp of the data acquisition process.
            survey_id (str): survey identifier. This is the same for every
                sample in a survey.
            sample_id (str): sample identifier. This is unique for each sample
                taken by the robot.
            vna_freq (str): string with the raw response of the VNA when
                requested of the frequency values in which data was acquired.
            vna_trace (str): string with the raw response of the VNA when
                requested of the acquired trace data.
        """
        # Parse the frequency response
        vna_freq = DataParsing.parse_vna_frequency(vna_freq)

        # Parse the trace response
        vna_trace_re, vna_trace_im = DataParsing.parse_vna_trace(
            vna_trace
        )

        # Store the data in the corresponding JSON file
        DataStorage.store_data(
            survey_dir,
            x_coord,
            y_coord,
            z_coord,
            antennae_height,
            timestamp,
            survey_id,
            sample_id,
            vna_freq,
            vna_trace_re,
            vna_trace_im
        )
