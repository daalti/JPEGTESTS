import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using 1PagePrintFaceDown.prn
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1PagePrintFaceDown.prn=7d89e836c8a035fd899fa9dd7e9d195670a4b681242bed3a911cfb656e5afb56
    +test_classification:System
    +name: test_pcl5_testfiles_1pageprintfacedown
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_1pageprintfacedown
        +guid:e5bbc4a3-8d3d-4c3c-b584-04bfc95ffc02
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_1pageprintfacedown(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7d89e836c8a035fd899fa9dd7e9d195670a4b681242bed3a911cfb656e5afb56', timeout=600)
    outputsaver.save_output()
