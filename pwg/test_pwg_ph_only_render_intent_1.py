import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only render intent-1 page from *PwgPhOnly-RenderIntent-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-RenderIntent-1.pwg=cc43a92afc41e8d4d558a9c089ac97397f31cec762711d551a72d0aa491f6add
    +name:test_pwg_ph_only_render_intent_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_render_intent_1_page
        +guid:67fd444e-02ea-4909-a55e-409890c0c113
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_render_intent_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cc43a92afc41e8d4d558a9c089ac97397f31cec762711d551a72d0aa491f6add')
    outputsaver.save_output()

    logging.info("PWG Ph Only Render Intent-1 - Print job completed successfully")
