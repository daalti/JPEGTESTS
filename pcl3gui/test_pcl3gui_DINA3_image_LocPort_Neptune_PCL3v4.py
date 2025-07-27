import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_DINA3_image_LocPort_Neptune_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3415
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DINA3_image_LocPort_Neptune_PCL3v4.prn=923cb9de885b1014d38b687628065985686a9b05aa5a8bf84dc634e25eb0ed20
    +test_classification:System
    +name:test_pcl3Gui_DINA3_image_LocPort_Neptune_PCL3v4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3Gui_DINA3_image_LocPort_Neptune_PCL3v4
        +guid:0589c958-7a6f-11eb-902b-7bccb3703d94
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3Gui_DINA3_image_LocPort_Neptune_PCL3v4(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify_multi('923cb9de885b1014d38b687628065985686a9b05aa5a8bf84dc634e25eb0ed20', 'SUCCESS', 1, 300)
    logging.info("Pcl3Gui DINA3_image_LocPort_Neptune_PCL3v4 - Print job completed successfully")
    
    expected_crc = ["0x7998988f"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("Pcl3Gui DINA3_image_LocPort_Neptune_PCL3v4 - Checksum(s) verified successfully")
