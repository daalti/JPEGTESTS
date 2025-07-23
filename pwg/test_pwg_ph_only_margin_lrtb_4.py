import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-MarginLRTB-4.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MarginLRTB-4.pwg=3d25660976b0d91353ffbe6e83ee768c666eebd538b75db24795c1a5bb97f384
    +name:test_pwg_phonly_margin_lrtb_4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_phonly_margin_lrtb_4
        +guid:6da8f806-b2f6-429c-af26-7e59a499768d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_phonly_margin_lrtb_4(setup_teardown, printjob, outputsaver, tray):
    # file size  Width:297039 & Height:209903 in microns.
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('3d25660976b0d91353ffbe6e83ee768c666eebd538b75db24795c1a5bb97f384', 'FAILED')
    outputsaver.save_output()
    tray.reset_trays()
