import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only media select by page size-3 page from *PwgPhOnly-MediaSelectByPageSize-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:400
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MediaSelectByPageSize-3.pwg=0e18539ec3981ad74c954226bae642fb00356def88f3870c2b7e0162180863ad
    +name:test_pwg_ph_only_media_select_by_page_size_3_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_media_select_by_page_size_3_page
        +guid:44e1c8da-a07f-4e52-9308-3e02703ff5e4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_media_select_by_page_size_3_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('any', default):
        tray.configure_tray(default, 'any', 'any')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('0e18539ec3981ad74c954226bae642fb00356def88f3870c2b7e0162180863ad', timeout =400)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PWG Ph Only Media Select by Page Size-3 - Print job completed successfully")
