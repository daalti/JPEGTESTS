import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ColorText.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ColorText.pcl=5cc544ffd5ea24b87b81a09c20733ea19d0ed267a5792b917fb4254fa8add16d
    +test_classification:System
    +name: test_pcl5_testfiles_text_colortext
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_text_colortext
        +guid:f773927b-bb39-4284-a3de-a29d764e9382
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_colortext(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5cc544ffd5ea24b87b81a09c20733ea19d0ed267a5792b917fb4254fa8add16d', timeout=600)
    outputsaver.save_output()
