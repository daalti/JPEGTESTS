import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print render intent-5 from *PwgCloudPrint-RenderIntent-5.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-RenderIntent-5.pwg=9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa
    +name:test_pwg_cloud_print_render_intent_5_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_render_intent_5_page
        +guid:6064d0ce-015f-4dac-b027-ab412c6007b6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_render_intent_5_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Render Intent-5 pagecompleted successfully")
