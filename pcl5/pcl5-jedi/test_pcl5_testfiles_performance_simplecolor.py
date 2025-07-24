import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using SimpleColor.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:SimpleColor.pcl=dd54fdf21eb1dd4d6d557007c2d920780219aaaaa413642aae10ec11688c6832
    +test_classification:System
    +name: test_pcl5_testfiles_performance_simplecolor
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_performance_simplecolor
        +guid:f1496833-cf8f-4bbc-870d-3e4842c8c21f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_performance_simplecolor(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dd54fdf21eb1dd4d6d557007c2d920780219aaaaa413642aae10ec11688c6832', timeout=600)
    outputsaver.save_output()
