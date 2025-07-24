import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using sv.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sv.pcl=71721637f42b191a95e6cedd94f74d540a453e9ca64a97e665f41519bc405322
    +test_classification:System
    +name: test_pcl5_testfiles_gl_sv
    +test:
        +title: test_pcl5_testfiles_gl_sv
        +guid:82f6fddc-c509-4953-acc4-dca10d7848a9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_sv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('71721637f42b191a95e6cedd94f74d540a453e9ca64a97e665f41519bc405322', timeout=600)
    outputsaver.save_output()
