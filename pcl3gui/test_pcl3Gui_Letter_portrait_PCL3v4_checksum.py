import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *Letter_portrait_PCL3v4.prn
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3208
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:Letter_portrait_PCL3v4.prn=6568e2ca2862e40d807c9c3a749434fa0d4b14143bdbb2019d68c1324f83807b
    +test_classification:System
    +name:test_pcl3Gui_Letter_portrait_PCL3v4_checksum
    +test:
        +title:test_pcl3Gui_Letter_portrait_PCL3v4_checksum
        +guid:c2d88469-c70c-4efa-b387-47ac529f04bc
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_Letter_portrait_PCL3v4_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('6568e2ca2862e40d807c9c3a749434fa0d4b14143bdbb2019d68c1324f83807b', timeout=300)
    logging.info("prn basic Image_Letter_portrait_PCL3v4.prn - Print job completed successfully")

    expected_crc = ["0x9cfbb"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("prn basic Image_Letter_portrait_PCL3v4.prn - Checksum(s) verified successfully")