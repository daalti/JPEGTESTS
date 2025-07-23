import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print render intent-1 from *PwgCloudPrint-RenderIntent-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-RenderIntent-1.pwg=9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa
    +name:test_pwg_cloud_print_render_intent_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_render_intent_1_page
        +guid:991eba9e-2281-43ac-a3a9-290d30fc366b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_render_intent_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9e2aacf9b339519a93db7657921de351642653776b93885fa81656319fc689fa')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Render Intent-1 pagecompleted successfully")
