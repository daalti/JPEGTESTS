import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ubmanage.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ubmanage.obj=696897992d28365856af5fe6bf7c340a1fca418c5e64f83ffd82187fc900c652
    +test_classification:System
    +name: test_pcl5_pcl_fontmgmt_ubmanage
    +test:
        +title: test_pcl5_pcl_fontmgmt_ubmanage
        +guid:2e75c030-f374-4c75-b622-d936145d1d46
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontmgmt_ubmanage(setup_teardown, printjob, outputsaver):
    printjob.print_verify('696897992d28365856af5fe6bf7c340a1fca418c5e64f83ffd82187fc900c652', timeout=600)
    outputsaver.save_output()
