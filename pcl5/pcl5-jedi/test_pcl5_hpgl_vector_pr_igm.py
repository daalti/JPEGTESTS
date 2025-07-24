import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pr_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pr_igm.obj=83cd80795911ec882d434d48a8b8b407d08433d4912cb4a3aef8bdb99120d1b8
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pr_igm
    +test:
        +title: test_pcl5_hpgl_vector_pr_igm
        +guid:abe22a04-144a-4b94-9d26-dcc8f46c01d1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pr_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('83cd80795911ec882d434d48a8b8b407d08433d4912cb4a3aef8bdb99120d1b8', timeout=600)
    outputsaver.save_output()
