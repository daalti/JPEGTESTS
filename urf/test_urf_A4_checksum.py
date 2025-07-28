import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *A4.urf
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:A4.urf=2b0adec1b1c778ae0f84c76a23f21347a055d2b39ed5b2ee09cd731d321dda06
    +test_classification:System
    +name:test_urf_A4_checksum
    +test:
        +title:test_urf_A4_checksum
        +guid:35d94be6-616b-11eb-9bed-a72ffc34aae3
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=URF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_A4_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('2b0adec1b1c778ae0f84c76a23f21347a055d2b39ed5b2ee09cd731d321dda06', timeout=300)
    logging.info("urf basic file A4.urf - Print job completed successfully")

    expected_crc = ["0x9430ae6e"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("urf basic file A4.urf - Checksum(s) verified successfully")
