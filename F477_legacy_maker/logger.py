from arcpy import ExecuteError, GetMessages, AddError
import logging
import sys, traceback

def timer(starttime, endtime, state=None):
    hours, rem = divmod(endtime - starttime, 3600)
    minutes, seconds = divmod(rem, 60)
    if state:
        print("\n**** end of the state {} task ****\n".format(state))
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

def create_error_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("*** arcpy_Error_Logger ***")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(r"./error_logger.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    return logger

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("*** arcpy_EVENT_Logger ***")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(r"./logger.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


def event_logger(log):

    '''
        A decorator that wraps the passed in function and logs
    arcpy events

    @param logger: The logging object
    '''

    def decorator(func):

        def wrapper(*args, **kwargs):
            msgs = "\n***********{}*****************\n".format(func.__name__)
            msgs += GetMessages()
            log.info(msgs)
            return func(*args, **kwargs)
        return wrapper

    return decorator



def arcpy_exception(log):

    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param log: The logging object
    """


    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except:
                # Get the traceback object
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]

                # Concatenate information together concerning the error into a message string
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "\n************* \n{}\n************* \n".format(GetMessages(2))

                # Return python error messages for use in script tool or Python window
                AddError(pymsg)
                AddError(msgs)

                # Print Python error messages for use in Python / Python window
                log.exception(pymsg)
                log.exception(msgs)

        return wrapper
    return decorator





