import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-MarginLRTB-5.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MarginLRTB-5.pwg=06c3a98244287f7cb60e448a13839364c570e66a75cf7b8834adc1d705de5eda
    +name:test_pwg_phonly_margin_lrtb_5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_phonly_margin_lrtb_5
        +guid:e324b445-d6b0-4881-8167-8c6a65a6a96d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_phonly_margin_lrtb_5(setup_teardown, printjob, outputsaver, tray):
    default_source = tray.get_default_source()

    if tray.is_size_supported('na_executive_7.25x10.5in', default_source):
        tray.configure_tray(default_source, 'na_executive_7.25x10.5in', 'stationery')

    printjob.print_verify('06c3a98244287f7cb60e448a13839364c570e66a75cf7b8834adc1d705de5eda', 'FAILED')
    outputsaver.save_output()
    outputsaver.clear_output()
    tray.reset_trays()
