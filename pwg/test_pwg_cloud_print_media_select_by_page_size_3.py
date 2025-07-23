import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg clould print media select by page size by 3 from *PwgCloudPrint-MediaSelectByPageSize-3.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-MediaSelectByPageSize-3.pwg=e07c54607a659835e4bbf1c98feb3496fa5cd8da8f55774cf712942ea13b6806
    +name:test_pwg_cloud_print_media_select_by_page_size_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_media_select_by_page_size_3
        +guid:edb87401-5149-4f01-9ead-4dcf823442dd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_media_select_by_page_size_3(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('e07c54607a659835e4bbf1c98feb3496fa5cd8da8f55774cf712942ea13b6806')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PWG Cloud Print Select By Page Size By 3completed successfully")
