import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job file tower_a1_3pages.rs
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-14986
    +timeout:500
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tower_a1_3pages.rs=ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689
    +test_classification:System
    +name:test_rs_multiple_pages_checksum
    +test:
        +title:test_rs_multiple_pages_checksum
        +guid:386893dc-6213-11eb-9a68-63ad8cbbed05
        +dut:
            +type:Emulator, Simulator
            +configuration:DocumentFormat=RasterStreamICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_multiple_pages_checksum(setup_teardown, printjob, outputsaver):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689', timeout=500)
    logging.info("tower_a1_3pages.rs - Print job completed successfully")

    expected_crc = ["0xf084787c", "0xf084787c", "0xf084787c"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("tower_a1_3pages.rs - Checksum(s) verified successfully")
