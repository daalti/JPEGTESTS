import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using gotopcl.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:gotopcl.obj=000aee3531b08ff203d5557809c6c7baa276eee98753297ad0b9fc600fd5d086
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_gotopcl
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_gotopcl
        +guid:22a4cb67-b1a7-436b-9b42-25264f310214
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_gotopcl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('000aee3531b08ff203d5557809c6c7baa276eee98753297ad0b9fc600fd5d086', timeout=900)
    outputsaver.save_output()
