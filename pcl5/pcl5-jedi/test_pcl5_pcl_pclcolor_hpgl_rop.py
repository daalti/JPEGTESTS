import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using hpgl_rop.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:hpgl_rop.obj=1fc3fb77d31c399a10b65524832ff694d2ed7631f260fcd4174834655e030e29
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_hpgl_rop
    +test:
        +title: test_pcl5_pcl_pclcolor_hpgl_rop
        +guid:721c1512-c52d-4970-b53d-0aad3b604a44
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_hpgl_rop(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1fc3fb77d31c399a10b65524832ff694d2ed7631f260fcd4174834655e030e29', timeout=600)
    outputsaver.save_output()
