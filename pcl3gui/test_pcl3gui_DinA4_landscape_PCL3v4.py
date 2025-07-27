import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_DinA4_landscape_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3415
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DinA4_landscape_PCL3v4.prn=fa994ad91007d3b0b96c65d81fb0873e54de81031d70b45e8b575f0d7b7d547c
    +test_classification:System
    +name:test_pcl3Gui_DinA4_landscape_PCL3v4_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3Gui_DinA4_landscape_PCL3v4_300dpi
        +guid:483ed719-8dc2-4beb-9307-0a811c8482ac
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3Gui_DinA4_landscape_PCL3v4_300dpi(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('fa994ad91007d3b0b96c65d81fb0873e54de81031d70b45e8b575f0d7b7d547c', 'SUCCESS', 1, 300)
    logging.info("Pcl3Gui DinA4_landscape_PCL3v4 - Print job completed successfully")
    
    expected_crc =  ['0x6249e9ac']
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("Pcl3Gui DinA4_landscape_PCL3v4 - Checksum(s) verified successfully")
