import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print render intent-2 from *PwgCloudPrint-RenderIntent-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-RenderIntent-2.pwg=dd7f181fe6ddc188a0951a2ca052bac60ab64874b7ebff57be9fc6abe316658e
    +name:test_pwg_cloud_print_render_intent_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_render_intent_2_page
        +guid:94a2d486-7213-4a3f-a3e9-ecf3c12c99e5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_render_intent_2_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dd7f181fe6ddc188a0951a2ca052bac60ab64874b7ebff57be9fc6abe316658e')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Render Intent-2 pagecompleted successfully")
