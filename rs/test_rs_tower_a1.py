import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job of file tower_a1.rs **
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-2765, LFPSWQAA-3262
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tower_a1.rs=abfae6b4e8b5597dd712c14e210626b3fc3f13e040610e704cd0cc2d760a92ab
    +test_classification:System
    +name:test_rs_tower_a1
    +test:
        +title:test_rs_tower_a1
        +guid:bd92b94a-7f73-4918-9f3f-00ad58fdd205
        +dut:
            +type:Emulator, Simulator
            +configuration:DocumentFormat=RasterStreamICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_tower_a1(setup_teardown, printjob, outputsaver):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('abfae6b4e8b5597dd712c14e210626b3fc3f13e040610e704cd0cc2d760a92ab', timeout=300)
    logging.info("tower_a1.rs - Print job completed successfully")

    expected_crc = ["0xf084787c"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("tower_a1.rs - Checksum(s) verified successfully")
