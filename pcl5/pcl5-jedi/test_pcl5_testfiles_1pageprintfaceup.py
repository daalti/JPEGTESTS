import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using 1PagePrintFaceUp.prn
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1PagePrintFaceUp.prn=4333a4934fba84c60149ddc27e543f5eef613a4daf846bdd15fd9ba5ab30745b
    +test_classification:System
    +name: test_pcl5_testfiles_1pageprintfaceup
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_1pageprintfaceup
        +guid:dd877a01-c011-4c9d-b65a-281d0858dabd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_1pageprintfaceup(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4333a4934fba84c60149ddc27e543f5eef613a4daf846bdd15fd9ba5ab30745b', timeout=600)
    outputsaver.save_output()
