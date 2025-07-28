import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *A0.urf
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:500
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:A0.urf=c885a8564bcbbfd436a7111de6b7cf01223be03db80f3e56de3ca0207e8e4955
    +test_classification:System
    +name:test_urf_A0_checksum
    +test:
        +title:test_urf_A0_checksum
        +guid:e2086c78-6169-11eb-a458-0325c3f30f71
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=URF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_A0_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('c885a8564bcbbfd436a7111de6b7cf01223be03db80f3e56de3ca0207e8e4955', timeout=300)
    logging.info("urf basic file A0.urf - Print job completed successfully")

    expected_crc = ["0x777cc6c7"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("urf basic file A0.urf - Checksum(s) verified successfully")
