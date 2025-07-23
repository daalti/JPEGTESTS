import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only margin LRTB-2 page from *PwgPhOnly-MarginLRTB-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MarginLRTB-2.pwg=3216316c80d86ef983489bcdfd4283ab1c86dcc1139fc242e3fb96fde8a9cd24
    +name:test_pwg_ph_only_margin_lrtb_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_margin_lrtb_2_page
        +guid:7758edc0-1a62-4e04-b78e-5fb48aa402ba
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_margin_lrtb_2_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3216316c80d86ef983489bcdfd4283ab1c86dcc1139fc242e3fb96fde8a9cd24', 'FAILED')
    outputsaver.save_output()

    logging.info("PWG Ph Only Margin LRTB-2 page - Print job completed successfully")
