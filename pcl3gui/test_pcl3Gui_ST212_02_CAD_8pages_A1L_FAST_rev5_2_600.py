import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file ST212-02-CAD-8pages-A1L.prn and verify
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-61462
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:ST212-02-CAD-8pages-A1L.prn=f3a4a9f2bd6004188327a10af183a48549810f0af6582062f9d6071b29a49b41
    +test_classification:System
    +name:test_pcl3Gui_ST212_02_CAD_8pages_A1L_FAST_rev5_2_600
    +test:
        +title:test_pcl3Gui_ST212_02_CAD_8pages_A1L_FAST_rev5_2_600
        +guid:2ec57ffb-b791-401e-9ae7-7914961a09e8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL3GUI&EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_ST212_02_CAD_8pages_A1L_FAST_rev5_2_600(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('f3a4a9f2bd6004188327a10af183a48549810f0af6582062f9d6071b29a49b41', 'SUCCESS', 800, 1)
    logging.info("ST212-02-CAD-8pages-A1L.prn - Print job completed successfully")

    expected_crc = ['0x892f2a11', '0x1bc1d627', '0xe3b35f44', '0x8e49dac3', '0xc9a3309', '0xeaac006c', '0xad82a273', '0x4000e6e4']

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("ST212-02-CAD-8pages-A1L.prn - Print job verified")
