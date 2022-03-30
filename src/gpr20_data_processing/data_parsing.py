"""This file contains the implementation of the data parsing module.

The data parsing module (DataParsing) contains the implementation of the
required functionalities to parse data from the VNA instrument of the
robot.
"""


class DataParsing(object):
    """Class to parse responses from the VNA instrument.

    This class contains the methods to parse the responses from the VNA. Two
    main methods are used for parsing the VNA response data depending on its
    type: frequency and trace. These methods will receive the raw response
    from the instrument and then convert it to structured values.
    """

    def parse_vna_trace(vna_trace):
        """Parse the VNA trace response from the VNA instrument.

        Receive the raw trace response from the VNA instrument and convert it
        to two (2) lists. The lists contain the real and imaginary components
        of the VNA trace response.

        Args:
            vna_trace (str): raw response from the VNA instrument when
                queried for the trace value.

        Returns:
            list: contains the real components of the trace reponse.
            list: contains the imaginary components of the trace response.
        """
        # Remove the header from response
        vna_trace = DataParsing.__remove_header(vna_trace)

        # Create the array with the numbers and data
        vna_trace = DataParsing.__create_array(vna_trace)

        # Create the arrays for storing real and imaginary values
        vna_trace_re, vna_trace_im = [], []

        # Iterate over the trace response
        for indx in range(len(vna_trace)):

            # Even index values are stored in the real-component list
            if indx % 2 == 0:

                # Append value into real-component list
                vna_trace_re.append(vna_trace[indx])

            # Odd index values are stored in the complex-component list
            if indx % 2 != 1:

                # Append value into complex-component list
                vna_trace_im.append(vna_trace[indx])

        # Return the lists
        return vna_trace_re, vna_trace_im

    def parse_vna_frequency(vna_freq):
        """Parse the VNA frequency response from the VNA instrument.

        Receive the VNA frequency response from the VNA instrument and convert
        it to a formatted list.

        Args:
            vna_freq (str): raw string response from the VNA instrument when
                queried for the trace frequency values.

        Returns:
            list: with the formatted frequency values of the VNA instrument
                trace.
        """
        # Remove the header from response
        vna_freq = DataParsing.__remove_header(vna_freq)

        # Create the array with the numbers and data
        vna_freq = DataParsing.__create_array(vna_freq)

        # Return formatted frequency list
        return vna_freq

    @staticmethod
    def __remove_header(vna_response):
        """Remove the header from the VNA response.

        This method removes the header as specified by the VNA documentation.
        The header consists of a hashtag character ('#'), followed by a number
        that specifies the header bytes length. The hashtag, the number and
        the header are removed from the response string.

        Returns:
            str: response string without the header.
        """
        # Remove the leading '#' character
        vna_response = vna_response[1:]

        # Get the header length in bytes
        header_len = int(vna_response[0])

        # Remove the header based on calculated length
        vna_response = vna_response[header_len+1:]

        # Return the response without header
        return vna_response

    @staticmethod
    def __create_array(vna_response):
        """Create a list with the retrieved data from the VNA.

        This method converts the VNA response string, without the header, to a
        python list containing the values formatted as float numbers.

        Args:
            vna_response (str): string with the values from the VNA response
                after removing the header.

        Returns:
            list: list with data from the VNA formatted as float numbers.
        """
        # Split the string on everry comma (',')
        vna_response = vna_response.split(',')

        # Convert the strings into float numbers
        vna_response = [
            float(vna_response[indx]) for indx in range(len(vna_response) - 1)
        ]

        # Return the list with the values
        return vna_response
