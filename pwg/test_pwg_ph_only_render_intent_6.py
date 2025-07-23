import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only render intent-6 page from *PwgPhOnly-RenderIntent-6.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-RenderIntent-6.pwg=c4d35be36d282ba3a7db6c91a005336e1733e73e18231144967306f5f42bced0
    +name:test_pwg_ph_only_render_intent_6_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_render_intent_6_page
        +guid:51e9607e-9915-4861-a927-933a0fd11750
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
def test_pwg_ph_only_render_intent_6_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c4d35be36d282ba3a7db6c91a005336e1733e73e18231144967306f5f42bced0')
    outputsaver.save_output()

    logging.info("PWG Ph Only Render Intent-6 - Print job completed successfully")
