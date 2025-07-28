import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter.urf=c1a5b2a1bc45c935ba09cede30b60c9b7277b459888f6acd753bb1012f44beb0
    +name:test_urf_letter
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_letter
        +guid:dfa8b5b4-3482-11eb-9dd9-e385460e7268
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_letter(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('c1a5b2a1bc45c935ba09cede30b60c9b7277b459888f6acd753bb1012f44beb0', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Letter - Print job completed successfully")
