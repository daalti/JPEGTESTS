import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600 
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-61462
    +timeout:800
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600.prn=6dc1f4dd93ceb76877a833d0dae2c1288c0668784aa302d174472c81304b4e19
    +test_classification:System
    +name:test_pcl3Gui_ST212_01_CAD_Tower_5pages_A1L_FAST_rev5_2_600
    +test:
        +title:test_pcl3Gui_ST212_01_CAD_Tower_5pages_A1L_FAST_rev5_2_600
        +guid:720cd486-7b2a-41b7-b8ff-c946f8b82356
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_ST212_01_CAD_Tower_5pages_A1L_FAST_rev5_2_600(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('6dc1f4dd93ceb76877a833d0dae2c1288c0668784aa302d174472c81304b4e19', 'SUCCESS', 800, 1)
    logging.info("ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")

    expected_crc = ["0x87d8ae1a", "0x5b0631e2", "0xed19c28e", "0xec1adf81", "0x3cad5711"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")
