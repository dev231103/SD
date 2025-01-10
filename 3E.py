import os
import logging
import uuid
import shutil
import time

# Set the base directory for Windows
Base = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals'

# List of companies, layers, and log levels
sCompanies = ['01-Vermeulen', '02-Krennwallner', '03-Hillman', '04-Clark']
sLayers = ['01-Retrieve', '02-Assess', '03-Process', '04-Transform', '05-Organise', '06-Report']
sLevels = ['debug', 'info', 'warning', 'error']

# Loop over each company
for sCompany in sCompanies:
    # Define the file path for the company
    sFileDir = os.path.join(Base, sCompany)  # Using os.path.join for proper path creation
    if not os.path.exists(sFileDir):
        os.makedirs(sFileDir)  # Create the directory if it doesn't exist

    # Loop over each layer within the company
    for sLayer in sLayers:
        log = logging.getLogger()  # Root logger

        # Remove any old handlers
        for hdlr in log.handlers[:]:
            log.removeHandler(hdlr)

        # Define the log directory for the current layer
        sFileDir = os.path.join(Base, sCompany, sLayer, 'Logging')  # Correct path for logging directory

        # If the directory exists, remove it and recreate
        if os.path.exists(sFileDir):
            shutil.rmtree(sFileDir)
        time.sleep(2)  # Wait for a short time before recreating the directory

        if not os.path.exists(sFileDir):
            os.makedirs(sFileDir)  # Create the log directory

        # Generate a unique key for the log file using UUID
        skey = str(uuid.uuid4())
        sLogFile = os.path.join(sFileDir, f'Logging_{skey}.log')  # Construct the full log file path
        print('Set up:', sLogFile)

        # Set up logging to file
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=sLogFile,
                            filemode='w')

        # Define a console handler for logging to the terminal (INFO and above)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        # Define a simpler format for console output
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)

        # Add the console handler to the root logger
        logging.getLogger('').addHandler(console)

        # Log an info message to show that the logger is set up
        logging.info('Practical Data Science is fun!')

        # Loop through different log levels and log messages accordingly
        for sLevel in sLevels:
            sApp = f'Application-{sCompany}-{sLayer}-{sLevel}'  # Logger name for each level
            logger = logging.getLogger(sApp)  # Create or get logger for this specific application/level

            if sLevel == 'debug':
                logger.debug('Practical Data Science logged a debugging message.')
            elif sLevel == 'info':
                logger.info('Practical Data Science logged information message.')
            elif sLevel == 'warning':
                logger.warning('Practical Data Science logged a warning message.')
            elif sLevel == 'error':
                logger.error('Practical Data Science logged an error message.')
