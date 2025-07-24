import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpminchit.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpminchit.obj=d6ce8bd9042896bfc3627860b28b3be9bb32ee77fb0b071dee8628e07eecab3c
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpminchit
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpminchit
        +guid:8d6ebe91-5761-454b-98c7-5f5ee89f942b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpminchit(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d6ce8bd9042896bfc3627860b28b3be9bb32ee77fb0b071dee8628e07eecab3c', timeout=600)
    outputsaver.save_output()
