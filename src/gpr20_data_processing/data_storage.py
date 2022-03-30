"""This module includes the storage means for the GPR-20 robot."""


import os
import json


class DataStorage(object):
    """Class to store data using the JSON format.

    The class main objective is to provide the means to store samples in a
    persistent storage with a consistent format. The class also provides
    methods to manage the folders in order to prevent errors from happening.
    """

    @staticmethod
    def store_data(survey_dir, x_coord, y_coord, z_coord, antennae_height,
                   timestamp, survey_id, sample_id, vna_freq, vna_trace_re,
                   vna_trace_im):
        """Store the robot data for a sample in the required format.

       In general, this method stores the data for the GPR-20 robot in the
       JSON format. The data content is received via the method parameters.
       The target folder is also received as a parameter.

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
            vna_freq (list): list with the frequency values in which data was
                acquired.
            vna_trace_re (list): list with the real components of the VNA
                trace data.
            vna_trace_im (list): list with the imaginary components of the VNA
                trace data.
        """
        # Create the data list
        data_list = []

        # Formats the data list
        for indx in range(len(vna_freq)):

            # Create the dictionary for a data element
            data_dict = {
                "freq_value": vna_freq[indx],
                "real_value": vna_trace_re[indx],
                "imaginary_value": vna_trace_im[indx]
            }

            # Append the dictionary to the data list
            data_list.append(data_dict)

        # Create the file dictionary
        file_dict = {
            "x_coord": x_coord,
            "y_coord": y_coord,
            "z_coord": z_coord,
            "antennae_height": antennae_height,
            "timestamp": timestamp,
            "survey_id": survey_id,
            "sample_id": sample_id,
            "data": data_list
        }

        # Convert the file dictionary into JSON string
        json_str = json.dumps(file_dict, indent=4)

        # Create the file name
        fname = "X{:06.2f}_Y{:06.2f}_Z{:06.2f}.json".format(
            x_coord,
            y_coord,
            z_coord
        )

        # Check that main folder exists
        main_dir = DataStorage.__check_main_folder()

        # Creates the survey folder path
        survey_path = main_dir + '/' + survey_dir

        # Check that survey folder exists
        DataStorage.__check_survey_folder(survey_path)

        # Open the file to write JSON string
        with open(survey_path + '/' + fname, 'w') as json_file:

            # Save the JSON string into file
            json_file.write(json_str)

    @staticmethod
    def __check_main_folder():
        """Check the main folder for storing GPR-20 surveys data.

        Firstly, the home folder full path is retrieved by asking the host
        operating system for it. Then, the data path is added to the home path
        in order to create the full data path. Finally, it is checked if the
        folder exists. If the folder exists, no further action is taken.
        Otherwise, the folder is created.

        Returns:
            str: full path to survey main folder. The main folder is located
                in the home directory, and uses the name 'gpr20_data'.
        """
        # Get the home directory path
        home_path = os.path.expanduser('~')

        # Define the main folder path
        main_folder = home_path + "/gpr20_data/"

        # Check if main directory exists
        main_dir_exists = os.path.exists(main_folder)

        # Create the directory if it does not exists
        if not main_dir_exists:

            # Create the main directory for storing surveys
            os.mkdir(main_folder)

        # Return the main folder full path
        return main_folder

    @staticmethod
    def __check_survey_folder(path):
        """Check if the survey forder exits and create it if needed.

        This method checks if the survey folder exists. If the folder exists,
        no action is taken. If the folder does not exists, it is created using
        the operating system library.

        Args:
            path (str): path to the folder that will be checked. The path
                corresponds to the survey folder instead of the main folder.
        """
        # Check if main directory exists
        survey_dir_exists = os.path.exists(path)

        # Create the directory if it does not exists
        if not survey_dir_exists:

            # Create the main directory for storing surveys
            os.mkdir(path)
