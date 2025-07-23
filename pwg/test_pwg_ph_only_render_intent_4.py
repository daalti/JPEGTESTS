import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only render intent-4 page from *PwgPhOnly-RenderIntent-4.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-RenderIntent-4.pwg=dd7f181fe6ddc188a0951a2ca052bac60ab64874b7ebff57be9fc6abe316658e
    +name:test_pwg_ph_only_render_intent_4_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_render_intent_4_page
        +guid:86a99cae-9f5d-42a9-8332-14a4238d3445
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_render_intent_4_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dd7f181fe6ddc188a0951a2ca052bac60ab64874b7ebff57be9fc6abe316658e')
    outputsaver.save_output()

    logging.info("PWG Ph Only Render Intent-4 - Print job completed successfully")
