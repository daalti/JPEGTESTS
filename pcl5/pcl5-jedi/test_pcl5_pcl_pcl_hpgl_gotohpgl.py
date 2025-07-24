import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using gotohpgl.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:gotohpgl.obj=f9797a736d8431c278b82c3789d0513be9935a1a4d4419eaceabd367793f9b65
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_gotohpgl
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_gotohpgl
        +guid:266f27ae-776f-4950-a742-2f811963ac12
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_gotohpgl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f9797a736d8431c278b82c3789d0513be9935a1a4d4419eaceabd367793f9b65', timeout=900)
    outputsaver.save_output()
