import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 11x17_Color_600 page from *11x17_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:11x17_Color_600.urf=cb3e64b9121a3a57179109cdee178a2079fb75aaf9fd9d28a43955886c63c973
    +name:test_urf_11x17_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_11x17_color_600_page
        +guid:b0f1e455-d0bf-4e3d-9c71-8408aa7234cb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_11x17_color_600_page(setup_teardown, printjob, outputsaver, tray):
    printjob.print_verify('cb3e64b9121a3a57179109cdee178a2079fb75aaf9fd9d28a43955886c63c973')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 11x17 Color 600 page - Print job completed successfully")
