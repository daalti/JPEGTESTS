import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using CollatedQTY2.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:CollatedQTY2.pcl=59a78929abeddd358bba107d87daa71324600b47904094e084b2e82508055ada
    +test_classification:System
    +name: test_pcl5_testfiles_collatedqty2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_collatedqty2
        +guid:5ba0b794-1530-4967-8274-67463da035df
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_collatedqty2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('59a78929abeddd358bba107d87daa71324600b47904094e084b2e82508055ada', timeout=600)
    outputsaver.save_output()
