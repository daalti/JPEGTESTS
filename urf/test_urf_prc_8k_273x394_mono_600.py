import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Prc_8k_273x394_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Prc_8k_273x394_Mono_600.urf=6227822ecaeb05b68022dcf47d15d14f01793b161f663ac7da2bd8773a62d9d8
    +name:test_urf_prc_8k_273x394_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_prc_8k_273x394_mono_600
        +guid:9cb2d237-42a7-4e60-8090-fae912c059b7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_prc_8k_273x394_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('roc_8k_10.75x15.5in', default):
        tray.configure_tray(default, 'roc_8k_10.75x15.5in', 'stationery')
    elif tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.print_verify('6227822ecaeb05b68022dcf47d15d14f01793b161f663ac7da2bd8773a62d9d8')
    outputsaver.save_output()
    tray.reset_trays()
