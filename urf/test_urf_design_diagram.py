import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Design Diagram urf from *DesignDiagram.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DesignDiagram.urf=9b06fded90efaed3e7382606d80136c54a1e0465f3a471e3cb5e0f954bbf171c
    +name:test_urf_design_diagram_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_design_diagram_page
        +guid:4c4dc5e6-9f71-4c00-bff9-a286539ff4dd
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
def test_urf_design_diagram_page(setup_teardown, printjob, outputsaver, tray):
    # TODO: In case of failure in the future, check for media size requested, load if supported
    printjob.print_verify('9b06fded90efaed3e7382606d80136c54a1e0465f3a471e3cb5e0f954bbf171c')
    outputsaver.save_output()

    logging.info("URF Design Diagram page - Print job completed successfully")
