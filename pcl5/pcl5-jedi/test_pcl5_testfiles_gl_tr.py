import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using tr.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tr.pcl=60ea0ae67dad0de32a05a3246f5792219a2935469c1a05116a484ae7c7b09eda
    +test_classification:System
    +name: test_pcl5_testfiles_gl_tr
    +test:
        +title: test_pcl5_testfiles_gl_tr
        +guid:c708ad71-bbda-44e8-b4dc-790a9f4b3e7d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_tr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('60ea0ae67dad0de32a05a3246f5792219a2935469c1a05116a484ae7c7b09eda', timeout=600)
    outputsaver.save_output()
