import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only margin LRTB-3 page from *PwgPhOnly-MarginLRTB-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MarginLRTB-3.pwg=4fe90562f2904985b2eb1d4f2ad810d8f2732951ebd0ea2d9ea6ffb12d646e81
    +name:test_pwg_ph_only_margin_lrtb_3_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_margin_lrtb_3_page
        +guid:315611cd-cfd8-478c-a790-d6fc8926f6c4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_margin_lrtb_3_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('4fe90562f2904985b2eb1d4f2ad810d8f2732951ebd0ea2d9ea6ffb12d646e81')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PWG Ph Only Margin LRTB-3 page - Print job completed successfully")
