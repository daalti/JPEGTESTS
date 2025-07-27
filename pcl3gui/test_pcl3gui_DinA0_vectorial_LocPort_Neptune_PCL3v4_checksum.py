import pytest
import logging
import time
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *DinA0_vectorial_LocPort_Neptune_PCL3v4.prn
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3413
    +timeout:350
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:DinA0_vectorial_LocPort_Neptune_PCL3v4.prn=7c58792c27c6a86acac9c38d48accd04cf48f8053907956f534b38a6e450f4bd
    +test_classification:System
    +name:test_pcl3gui_DinA0_vectorial_LocPort_Neptune_PCL3v4_checksum
    +test:
        +title:test_pcl3gui_DinA0_vectorial_LocPort_Neptune_PCL3v4_checksum
        +guid:8e6bb050-cfb6-49f4-8419-856b061dbc48
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_DinA0_vectorial_LocPort_Neptune_PCL3v4_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('7c58792c27c6a86acac9c38d48accd04cf48f8053907956f534b38a6e450f4bd', 'SUCCESS', 300, 1)
    logging.info("PRN DinA0_vectorial_LocPort_Neptune_PCL3v4 - Print job completed successfully")

    expected_crc = ["0x68f21c10"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("PRN DinA0_vectorial_LocPort_Neptune_PCL3v4 - Print job completed successfully")
