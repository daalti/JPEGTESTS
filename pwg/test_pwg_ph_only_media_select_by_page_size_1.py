import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only media select by page size-1 page from *PwgPhOnly-MediaSelectByPageSize-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MediaSelectByPageSize-1.pwg=9e4b1a470ab6a398228837930929ceb1eadabf42574fb64f501dfc1f2845a8ce
    +name:test_pwg_ph_only_media_select_by_page_size_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_media_select_by_page_size_1_page
        +guid:62827628-43ab-4d39-8505-5d95fe396008
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_media_select_by_page_size_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9e4b1a470ab6a398228837930929ceb1eadabf42574fb64f501dfc1f2845a8ce')
    outputsaver.save_output()

    logging.info("PWG Ph Only Media Select by Page Size-1 - Print job completed successfully")
