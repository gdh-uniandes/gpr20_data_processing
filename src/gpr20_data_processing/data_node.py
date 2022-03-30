"""ROS interface for the data processing utility of the GPR-20 software stack.

This class implements the communication mechanisms for the GPR-20 data
processing utility. The class uses a service to receive the request to process
and store GPR-20 robot data.
"""

import rospy
from gpr20_data_processing.data_processing import DataProcessing
from gpr20_msgs.srv import ProcessingStoreData, ProcessingStoreDataResponse


class DataNode(object):
    """Class that provides the ROS communication for the data processing.

    This class allows to use the data processing pipeline within the ROS
    framework. This consists of using the data processing as a ROS node with
    a service that provides the communication mechanism.
    """

    def __init__(self):
        """Initialize the ROS interface class for the data processing utility.

        The initializer definites and launches the ROS node for data
        processing, while defining the data processing service. A ROS spin is
        used to prevent the node from exiting.
        """
        # Initialize the data processing node
        rospy.init_node("data_processing", anonymous=False)

        # Define the service for receiving the processing data request
        rospy.Service(
            "processing_store_data",
            ProcessingStoreData,
            self.__store_data_handler
        )

        # Prevent the node from exiting
        rospy.spin()

    def __store_data_handler(self, srv):
        """Hanlde the request to store data of GPR-20.

        The handler class the processing implementation of the data pipeline
        from a non-ROS class. An empty response is returned to indicate that
        the request was retrieved.

        Args:
            srv (gpr20_msgs.srv.ProcessingStoreData): service message request
                to store sample data.

        Returns:
            gpr20_msgs.srv.ProcessingStoreDataResponse: empty response to
                indicate that process has finished.
        """
        # Call the method to store data in file
        DataProcessing.process_data(
            srv.survey_dir,
            srv.x_coord,
            srv.y_coord,
            srv.z_coord,
            srv.antennae_height,
            srv.timestamp,
            srv.survey_id,
            srv.sample_id,
            srv.vna_freq,
            srv.vna_trace
        )

        # Return the request response
        return ProcessingStoreDataResponse()
