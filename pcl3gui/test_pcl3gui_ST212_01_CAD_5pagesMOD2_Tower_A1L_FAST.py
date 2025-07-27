import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job file ST212-01-CAD-5pages-Tower-A1L checksum
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-4385
    +timeout:700
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:ST212-01-CAD-5pagesMOD2-Tower-A1L-FAST.prn=b3eff59492252078bb8ab0d4c295e860c2ed71ce0572414147ceac92fc486e42
    +test_classification:System
    +name:test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_300dpi
    +test:
        +title:test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_300dpi
        +guid:592a01c6-11a1-4e76-8958-b900854e750e
        +dut:
            +type:Emulator, Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_300dpi(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('b3eff59492252078bb8ab0d4c295e860c2ed71ce0572414147ceac92fc486e42', 'SUCCESS', 700, 1)
    logging.info("test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_checksum - Print job completed successfully")

    expected_crc = ['0xd3efd4f7', '0x8e46b3bf', '0xbb89a8ad', '0x7b5a5ffd', '0xcc1c981f']

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_checksum' - Print job completed successfully")


