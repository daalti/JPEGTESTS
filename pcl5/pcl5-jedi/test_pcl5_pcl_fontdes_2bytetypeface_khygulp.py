import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulp.obj=8664cfb7eb34c03e9dbe13a9befbf51a96d9721d4d2a4a1417c8cd1a9b423963
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulp
        +guid:176c154b-408a-4b69-8d63-318745d1fa95
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8664cfb7eb34c03e9dbe13a9befbf51a96d9721d4d2a4a1417c8cd1a9b423963', timeout=600)
    outputsaver.save_output()
