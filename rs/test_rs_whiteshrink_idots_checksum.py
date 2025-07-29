import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print corner case job with white content and check WhiteShrink processing gives the right output
    +test_tier:1
    +is_manual:False
    +reqid:LFPPOS10987
    +timeout:500
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tear_effect_plus_wspot_idots_OF60_14p_final.rs=5873062d721fa67dc0f3e0ff53de555af5f5bf186b29d343948da19456bad562
    +test_classification:System
    +name:test_rs_whiteshrink_idots_checksum
    +test:
        +title:test_rs_whiteshrink_idots_checksum
        +guid:7415297c-6509-11ed-b18c-e3b6cb7bfaf5
        +dut:
            +type:Simulator, Emulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_whiteshrink_idots_checksum(setup_teardown, printjob, outputsaver):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify("5873062d721fa67dc0f3e0ff53de555af5f5bf186b29d343948da19456bad562", timeout=500)
    logging.info("RS tear_effect_plus_wspot_idots_OF60_14p_final - Print job completed successfully")

    expected_crc = ["0x2d369819"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("RS tear_effect_plus_wspot_idots_OF60_14p_final - Checksum(s) verified successfully")



@pytest.fixture()
def checkpoints(tcl):

    levels = ["a", "b", "c", "d"]

    # Temporary - Enabling all checkpoint levels for debugging intermittency
    logging.info("Temporary - Enabling all checkpoint levels for debugging intermittency")
    for l in levels:
        command = "Debug PUB_setFilterLevelAcrossAllDomains "+l+" true"
        tcl.execute(command)

    yield

    # Temporary - Disabling all previously enabled checkpoint levels for debugging intermittency
    logging.info("Temporary - Disabling all previously enabled checkpoint levels for debugging intermittency")
    for l in levels:
        command = "Debug PUB_setFilterLevelAcrossAllDomains "+l+" false"
        tcl.execute(command)