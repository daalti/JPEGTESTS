import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job on roll PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:LFPSWQAA-4560
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printOnroll.pcl=1e2d69d97d836018adf7be895a70abcdd0750b7af5041e185ded88b3e0bcfc4e
    +name:test_pcl3gui_print_on_roll
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_print_on_roll
        +guid:62fa8ede-3305-11ec-ab1a-03f88c15de79
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI&DeviceClass=MFP & MediaInputInstalled=MainRoll
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_print_on_roll(setup_teardown, printjob, outputsaver, udw):
    printjob.print_verify('1e2d69d97d836018adf7be895a70abcdd0750b7af5041e185ded88b3e0bcfc4e','SUCCESS', 120, 1)
    outputsaver.save_output()
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')

    logging.info("PCL3GUI print on roll successfully")
