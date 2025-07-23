import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only render intent-2 page from *PwgPhOnly-RenderIntent-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-RenderIntent-2.pwg=9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa
    +name:test_pwg_ph_only_render_intent_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_render_intent_2_page
        +guid:56b0c9f5-990a-43bf-b148-1e80afe6f6c3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_render_intent_2_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa')
    outputsaver.save_output()

    logging.info("PWG Ph Only Render Intent-2 - Print job completed successfully")
