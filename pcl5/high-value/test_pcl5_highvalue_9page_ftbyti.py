import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 9Page_ftbyti.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:9Page-ftbyti.obj=2ee7645664eae948a11385c85d6f4f7d14eda31da7dfbcc807cf527322807f6e
    +test_classification:System
    +name: test_pcl5_highvalue_9page_ftbyti
    +test:
        +title: test_pcl5_highvalue_9page_ftbyti
        +guid:d3019ee6-5fec-4daf-bc53-4dce12bd651d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_9page_ftbyti(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2ee7645664eae948a11385c85d6f4f7d14eda31da7dfbcc807cf527322807f6e')
    outputsaver.save_output()
