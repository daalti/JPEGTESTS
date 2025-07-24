import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using lf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lf.obj=349072e095fea4ece5e20548b808fe96a191345b31c8ad46c55007e83a25d85f
    +test_classification:System
    +name: test_pcl5_pcl_cap_lf
    +test:
        +title: test_pcl5_pcl_cap_lf
        +guid:11565f71-806a-4efd-94e8-a1104a0cc1cc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cap_lf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('349072e095fea4ece5e20548b808fe96a191345b31c8ad46c55007e83a25d85f', timeout=600)
    outputsaver.save_output()
