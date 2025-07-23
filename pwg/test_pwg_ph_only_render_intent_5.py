import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only render intent-5 page from *PwgPhOnly-RenderIntent-5.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-RenderIntent-5.pwg=fa19a7a725a589f94316df74a80ca173b294c5512a8f5d6349430db09e9ead36
    +name:test_pwg_ph_only_render_intent_5_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_render_intent_5_page
        +guid:7dd460c5-6b9a-4802-9f05-b9cfe9d60047
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_render_intent_5_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fa19a7a725a589f94316df74a80ca173b294c5512a8f5d6349430db09e9ead36')
    outputsaver.save_output()

    logging.info("PWG Ph Only Render Intent-5 - Print job completed successfully")
