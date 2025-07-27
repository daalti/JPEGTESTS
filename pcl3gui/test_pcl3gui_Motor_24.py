import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of PCL of Motor_24 Page from *Motor_24.pcl file
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3207
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Motor_24.pcl=fd3f12e1ef4332a1722cfb3f0211d338dddfb278f2e31f7df6b2c53509465624
    +test_classification:System
    +name:test_pcl3gui_Motor_24
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_Motor_24
        +guid:c60d9147-8977-4557-84b9-d649607a18ab
        +dut:
            +type:Simulator
            +configuration: PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3gui_Motor_24(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('fd3f12e1ef4332a1722cfb3f0211d338dddfb278f2e31f7df6b2c53509465624','SUCCESS', 1, 200)
    logging.info("PCL Motor_24 - Print job completed successfully")
    
    expected_crc = ["0xb2f7e74b"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("PCL Motor_24 - Checksum(s) verified successfully")
