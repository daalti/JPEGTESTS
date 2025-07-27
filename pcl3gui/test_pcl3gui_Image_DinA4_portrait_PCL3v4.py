import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of PRN of Image_DinA4_portrait_PCL3v4 Page from *Image_DinA4_portrait_PCL3v4.prn file
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3387
    +timeout:120
    +asset:LFP
    +test_framework:TUF
    +external_files:Image_DinA4_portrait_PCL3v4.prn=52949853ab1b37d10ddadba1d127cecac34fd82c956c46e733d88196ae915ca5
    +test_classification:System
    +name:test_pcl3gui_Image_DinA4_portrait_PCL3v4
    +test:
        +title:test_pcl3gui_Image_DinA4_portrait_PCL3v4
        +guid:40ad3a1b-8439-4f4b-9bd3-3f8cbe6e669b
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3gui_Image_DinA4_portrait_PCL3v4(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('52949853ab1b37d10ddadba1d127cecac34fd82c956c46e733d88196ae915ca5', 'SUCCESS', 1, 120)
    logging.info("PRN Image_DinA4_portrait_PCL3v4 - Print job completed successfully")
    
    expected_crc = ["0x206da19e"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("PRN Image_DinA4_portrait_PCL3v4 - Checksum(s) verified successfully")
