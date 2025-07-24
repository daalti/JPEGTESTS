import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using effwin2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:effwin2.obj=dc084abcc30b9ea6c54893bd83db50b99cf14d433216deb77b91581290c983bb
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_effwin2
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_effwin2
        +guid:5747199e-63b3-418f-82f4-3e585f8300ad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_effwin2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dc084abcc30b9ea6c54893bd83db50b99cf14d433216deb77b91581290c983bb', timeout=900)
    outputsaver.save_output()
