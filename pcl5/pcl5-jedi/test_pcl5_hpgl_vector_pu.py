import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pu.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pu.obj=ca31ae11adc0b4d72a331334d59e3a58c1858b8ff9e5b0643ad15c8e34905b91
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pu
    +test:
        +title: test_pcl5_hpgl_vector_pu
        +guid:48149c99-f47f-4658-ac0a-9115d7b4bdb8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pu(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ca31ae11adc0b4d72a331334d59e3a58c1858b8ff9e5b0643ad15c8e34905b91', timeout=600)
    outputsaver.save_output()
