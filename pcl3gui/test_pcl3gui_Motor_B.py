import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of PCL of Motor_B Page from *Motor_B.pcl file
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3207
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Motor_B.pcl=d033f006025aa34152da94073400a42f575592eb68e98eee9980081d9e0d607e
    +test_classification:System
    +name:test_pcl3gui_Motor_B
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_Motor_B
        +guid:4c6ca63c-9e5f-4e9b-9061-839544e9910d
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3gui_Motor_B(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('d033f006025aa34152da94073400a42f575592eb68e98eee9980081d9e0d607e','SUCCESS', 1, 240)
    logging.info("PCL Motor_B - Print job completed successfully")
    
    expected_crc = ["0x3dbba7f7"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("PCL Motor_B - Checksum(s) verified successfully")
