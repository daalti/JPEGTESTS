import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcpmingit.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcpmingit.obj=f278735a3e74e9b94605dd26dd8bfe16a1f9b58b9bc8788501a74cb8611cf82f
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingit
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingit
        +guid:60c8d5e1-f1e4-4dd6-b2bc-94f1722250ae
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcpmingit(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f278735a3e74e9b94605dd26dd8bfe16a1f9b58b9bc8788501a74cb8611cf82f', timeout=600)
    outputsaver.save_output()
