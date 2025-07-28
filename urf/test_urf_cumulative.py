import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of cumulative urf from *cumulative.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:cumulative.urf=35fa00f34c142dfedb608319e364efe600d48292b83382b7e1768e1bc65b8f24
    +name:test_urf_cumulative_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_cumulative_page
        +guid:9da4882b-5c75-4ee2-98cf-2221e63cabed
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_cumulative_page(setup_teardown, printjob, outputsaver, tray):
    # TODO: In case of failure in the future, check for media size requested, load if supported
    printjob.print_verify('35fa00f34c142dfedb608319e364efe600d48292b83382b7e1768e1bc65b8f24', timeout=600)
    outputsaver.save_output()

    logging.info("URF Cumulative page - Print job completed successfully")
