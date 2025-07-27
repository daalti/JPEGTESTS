import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_DINA1_vectorial_LocPort_Neptune_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3415
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DINA1_vectorial_LocPort_Neptune_PCL3v4.prn=cee226ca88fd3cebf49767a044e66bd6f4fe9e3d94fe41e59cc125e814b791c2
    +test_classification:System
    +name:test_pcl3Gui_DINA1_vectorial_LocPort_Neptune_PCL3v4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3Gui_DINA1_vectorial_LocPort_Neptune_PCL3v4
        +guid:94465118-7a68-11eb-9b71-1f940aefa37b
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3Gui_DINA1_vectorial_LocPort_Neptune_PCL3v4(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('cee226ca88fd3cebf49767a044e66bd6f4fe9e3d94fe41e59cc125e814b791c2','SUCCESS', 1, 200)
    logging.info("PRN DINA1_vectorial_LocPort_Neptune_PCL3v4 - Print job completed successfully")
    
    expected_crc = ["0xfb9b640b"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("PRN DINA1_vectorial_LocPort_Neptune_PCL3v4 - Checksum(s) verified successfully")
