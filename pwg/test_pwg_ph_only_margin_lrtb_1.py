import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only margin LRTB-1 page from *PwgPhOnly-MarginLRTB-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MarginLRTB-1.pwg=85adf3bb7ab0d844625e6d30efa1a23b624aa796cf17c99301464ea14bf75d70
    +name:test_pwg_ph_only_margin_lrtb_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_margin_lrtb_1_page
        +guid:a81a95df-4f4e-497f-9cc3-74c7dcad3c85
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
def test_pwg_ph_only_margin_lrtb_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('85adf3bb7ab0d844625e6d30efa1a23b624aa796cf17c99301464ea14bf75d70')
    outputsaver.save_output()

    logging.info("PWG Ph Only Margin LRTB-1 page - Print job completed successfully")
