import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of PRN of DinA4_portrait_PCL3v4 Page from *DinA4_portrait_PCL3v4.prn file
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3387
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DinA4_portrait_PCL3v4.prn=4310ea462c1447ae96b04cd713cc458d97897c269a102dc02ee46a1576754b16
    +test_classification:System
    +name:test_pcl3gui_DinA4_portrait_PCL3v4_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_DinA4_portrait_PCL3v4_300dpi
        +guid:2d9ef5c5-f35b-4d1c-be1b-c7f2ff45c23d
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3gui_DinA4_portrait_PCL3v4_300dpi(setup_teardown, printjob, outputsaver, tray):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('4310ea462c1447ae96b04cd713cc458d97897c269a102dc02ee46a1576754b16', 'SUCCESS', 1, 120)
    logging.info("PRN DinA4_portrait_PCL3v4 - Print job completed successfully")
    
    expected_crc = ['0x45982007']
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("PRN DinA4_portrait_PCL3v4 - Checksum(s) verified successfully")
