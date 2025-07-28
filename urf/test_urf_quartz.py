import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Quartz Page from *Quartz.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Quartz.urf=a3696c8f81d2fafe6d0934e4a70ee6e485a6043f4ec7de1c0627843d68d09968
    +name:test_urf_quartz_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_quartz_page
        +guid:945343ae-b4eb-4780-924e-11d3a6fb89ba
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_quartz_page(setup_teardown, printjob, outputsaver, tray):
    # TODO: In case of failure in the future, check for media size requested, load if supported
    printjob.print_verify('a3696c8f81d2fafe6d0934e4a70ee6e485a6043f4ec7de1c0627843d68d09968')
    outputsaver.save_output()

    logging.info("URF Quartz Page - Print job completed successfully")
