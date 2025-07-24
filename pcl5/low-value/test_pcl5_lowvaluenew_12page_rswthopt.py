import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 12Page_rswthopt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:12Page-rswthopt.obj=e8fa3aff351a74d9077488f1682f549ae4f1fa81966860dd98068dc8b088cbe5
    +test_classification:System
    +name: test_pcl5_lowvaluenew_12page_rswthopt
    +test:
        +title: test_pcl5_lowvaluenew_12page_rswthopt
        +guid:be30f4ef-10f5-420e-8c5e-2790053c5acb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_12page_rswthopt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e8fa3aff351a74d9077488f1682f549ae4f1fa81966860dd98068dc8b088cbe5', timeout=600)
    outputsaver.save_output()
