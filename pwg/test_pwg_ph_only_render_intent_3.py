import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only render intent-3 page from *PwgPhOnly-RenderIntent-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-RenderIntent-3.pwg=d9f1d34b6022a5c768dca712538601a2363d8600992c4ad4aa31eabe640c4414
    +name:test_pwg_ph_only_render_intent_3_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_render_intent_3_page
        +guid:7bbda80f-0be4-406c-a798-c7339a5d48d5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_render_intent_3_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d9f1d34b6022a5c768dca712538601a2363d8600992c4ad4aa31eabe640c4414')
    outputsaver.save_output()

    logging.info("PWG Ph Only Render Intent-3 - Print job completed successfully")
