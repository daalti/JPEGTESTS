import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print render intent-6 from *PwgCloudPrint-RenderIntent-6.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-RenderIntent-6.pwg=9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa
    +name:test_pwg_cloud_print_render_intent_6_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_render_intent_6_page
        +guid:f6a24fe4-4121-403c-aa26-716fa93aa87c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_render_intent_6_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Render Intent-6 pagecompleted successfully")
