import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Fire Letter Landscape from *FreeformUserManual.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:FreeformUserManual.urf=7cca274f741d66f0e553b404ca995d5eb45064a1f3233d121715ed0ecf034685
    +name:test_urf_free_form_user_manual_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_free_form_user_manual_page
        +guid:94a1765f-1e73-4e7c-9c7a-23247acc4b80
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_free_form_user_manual_page(setup_teardown, printjob, outputsaver, tray):
    # file size  Width:215900 & Height:279400 in microns, should configure tray with na_letter_8.5x11in 
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('7cca274f741d66f0e553b404ca995d5eb45064a1f3233d121715ed0ecf034685', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Free form User Manual page - Print job completed successfully")
