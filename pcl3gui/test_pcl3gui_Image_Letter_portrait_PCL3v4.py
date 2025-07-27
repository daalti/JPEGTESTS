import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_Image_Letter_portrait_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3422
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Image_Letter_portrait_PCL3v4.prn=6d5b5d2e4317a3c67a6069d96055cbd703bd7ead3c3135cef30b5980d2507a92
    +test_classification:System
    +name:test_pcl3Gui_Image_Letter_portrait_PCL3v4_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3Gui_Image_Letter_portrait_PCL3v4_300dpi
        +guid:c1fb91c1-4937-4c2b-8a74-3a595153a3f6
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$ 
"""

def test_pcl3Gui_Image_Letter_portrait_PCL3v4_300dpi(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('6d5b5d2e4317a3c67a6069d96055cbd703bd7ead3c3135cef30b5980d2507a92', 'SUCCESS', 1, 300)
    logging.info("Pcl3Gui Image_Letter_portrait_PCL3v4 - Print job completed successfully")
    
    expected_crc = ['0x193bec4b']
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("Pcl3Gui Image_Letter_portrait_PCL3v4 - Checksum(s) verified successfully")
