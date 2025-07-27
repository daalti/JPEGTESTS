import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:500
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:DinA1_image_LocPort_Neptune_PCL3v4.prn=d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610
    +test_classification:System
    +name:test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4_checksum
    +test:
        +title:test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4_checksum
        +guid:483a9284-6177-11eb-9972-f301bb19bb9b
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    printjob.print_verify('d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610', timeout=500)
    logging.info("Pcl3Gui DinA1_image_LocPort_Neptune_PCL3v4 - Print job completed successfully")

    expected_crc = ["0x4c84272"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("Pcl3Gui DinA1_image_LocPort_Neptune_PCL3v4 - Print job completed successfully")