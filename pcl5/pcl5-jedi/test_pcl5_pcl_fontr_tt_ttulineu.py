import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttulineu.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttulineu.obj=677424c246b309d6dcd9c57cb5865695e348daa01c64080d0e191c21ecf02ad3
    +test_classification:System
    +name: test_pcl5_pcl_fontr_tt_ttulineu
    +test:
        +title: test_pcl5_pcl_fontr_tt_ttulineu
        +guid:826ec9e4-66b7-4965-9b5a-64d8137cf5ff
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_tt_ttulineu(setup_teardown, printjob, outputsaver):
    printjob.print_verify('677424c246b309d6dcd9c57cb5865695e348daa01c64080d0e191c21ecf02ad3', timeout=600)
    outputsaver.save_output()
