import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ar_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ar_igm.obj=747500ceea43af4cea4eecba2423e27cc61206f92895204e790dbc31c91d8807
    +test_classification:System
    +name: test_pcl5_hpgl_vector_ar_igm
    +test:
        +title: test_pcl5_hpgl_vector_ar_igm
        +guid:3168ed38-561c-4a09-91c5-7c92f7a39b8b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_ar_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('747500ceea43af4cea4eecba2423e27cc61206f92895204e790dbc31c91d8807', timeout=600)
    outputsaver.save_output()
