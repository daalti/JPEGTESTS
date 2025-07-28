import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Stacks Page from *Stacks.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Stacks.urf=6b799b542481d4697a58e9f6ec04aa8ef5ff1528ab3145a24eea08d68201517f
    +name:test_urf_stacks_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_stacks_page
        +guid:737db06b-33da-4051-8719-af4b27e7ec5b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_stacks_page(setup_teardown, printjob, outputsaver, tray):
    # TODO: In case of failure in the future, check for media size requested, load if supported
    printjob.print_verify('6b799b542481d4697a58e9f6ec04aa8ef5ff1528ab3145a24eea08d68201517f')
    outputsaver.save_output()

    logging.info("URF Stacks Page - Print job completed successfully ")
