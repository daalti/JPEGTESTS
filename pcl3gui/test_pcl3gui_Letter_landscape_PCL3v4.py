import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_Letter_landscape_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3422
    +timeout:300
    +asset:LFP
    +test_framework:TUF
    +external_files:Letter_landscape_PCL3v4.prn=8fbde5ad03e851f1e228f6b235d73ce855e8329a70b026b3ef3fa24689c773a0
    +test_classification:System
    +name:test_pcl3Gui_Letter_landscape_PCL3v4
    +test:
        +title:test_pcl3Gui_Letter_landscape_PCL3v4
        +guid:33829738-7b3f-11eb-8e05-27c4b5895762
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3Gui_Letter_landscape_PCL3v4(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify_multi('8fbde5ad03e851f1e228f6b235d73ce855e8329a70b026b3ef3fa24689c773a0','SUCCESS', 1, 300)
    logging.info("Pcl3Gui Letter_landscape_PCL3v4 - Print job completed successfully")
    
    expected_crc = ["0xb03f5e3"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("Pcl3Gui Letter_landscape_PCL3v4 - Checksum(s) verified successfully")
