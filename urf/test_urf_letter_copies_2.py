import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf letter with copies set as 2
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-128385
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter_copies_2.prn=1448cb1193e618d83f84fa66a2f9a03e1d0a0ce8fd916bed87421052f50dcb70
    +name:test_urf_letter_copies_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_letter_copies_2
        +guid:786aca2d-780d-4013-84ce-cba59f5fd213
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_letter_copies_2(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('1448cb1193e618d83f84fa66a2f9a03e1d0a0ce8fd916bed87421052f50dcb70', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Letter - Print job with 2 copies completed successfully")
