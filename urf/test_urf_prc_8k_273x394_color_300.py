import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Prc 8k 273x394 Color 300 Page from *Prc_8k_273x394_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Prc_8k_273x394_Color_300.urf=ec7d87c728ddf6f9ca94c420362888e2e53c979220ce1d09b0166c63aa0d0f62
    +name:test_urf_prc_8k_273x394_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_prc_8k_273x394_color_300_page
        +guid:afce1c3f-5535-441e-a907-318a86b98b3d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_prc_8k_273x394_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('roc_8k_10.75x15.5in', default):
        tray.configure_tray(default, 'roc_8k_10.75x15.5in', 'stationery')
    elif tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.print_verify('ec7d87c728ddf6f9ca94c420362888e2e53c979220ce1d09b0166c63aa0d0f62')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Prc 8k 273x394 Color 300 Page - Print job completed successfully")
