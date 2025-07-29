import pytest
import logging
import time

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_packets_cmykw_whiteshrink
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-62762
    +timeout:900
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tear_effect_plus_wspot_Inv_OF60_14p_Choke3px.rs=a86aea37bb0395ef38fd9339d6794922448db2f51a040f92b28776eb38176f88
    +test_classification:System
    +name:test_rs_packets_cmykw_whiteshrink
    +test:
        +title:test_rs_packets_cmykw_whiteshrink
        +guid:f12a60aa-fa3e-43f6-a90a-f526aff98fc4
        +dut:
            +type:Simulator, Emulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.timeout(900)
def test_rs_packets_cmykw_whiteshrink(setup_teardown, printjob, outputsaver):

    printjob.print_verify(
        'a86aea37bb0395ef38fd9339d6794922448db2f51a040f92b28776eb38176f88', timeout=850)
    outputsaver.save_output()

    logging.info("RasterStream job finished")



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