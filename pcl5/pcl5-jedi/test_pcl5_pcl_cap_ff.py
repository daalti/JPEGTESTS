import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ff.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ff.obj=e88d639adac70b0bd1608bd14e6b5ae3087ed223c2dc4b66d369920ae65477b6
    +test_classification:System
    +name: test_pcl5_pcl_cap_ff
    +test:
        +title: test_pcl5_pcl_cap_ff
        +guid:30d94ff2-4ec9-422c-ac24-b609d2174d7c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cap_ff(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e88d639adac70b0bd1608bd14e6b5ae3087ed223c2dc4b66d369920ae65477b6', timeout=600)
    outputsaver.save_output()
